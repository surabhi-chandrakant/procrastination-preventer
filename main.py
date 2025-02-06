# File: main.py
import time
import logging
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import threading
import json
import os
from PIL import ImageGrab
import torch
from transformers import pipeline
import cv2
import numpy as np
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('activity_log.txt'),
        logging.StreamHandler()
    ]
)

class ProcrastinationPreventer:
    def __init__(self):
        self.intended_activities = []
        self.monitoring = False
        self.log_data = []
        self.screenshot_interval = 300  # 5 minutes in seconds
        
        # Initialize common work applications
        self.work_applications = {
            'text_editors': [
                'notepad', 'sublime', 'atom', 'vim', 'emacs', 
                'notepad++', 'textmate', 'brackets', 'ultraedit',
                'gedit', 'kate', 'nano'
            ],
            'browsers': [
                'chrome', 'firefox', 'safari', 'edge', 'opera',
                'brave', 'vivaldi'
            ],
            'terminals': [
                'terminal', 'cmd', 'powershell', 'bash', 'iterm',
                'konsole', 'xterm', 'gnome-terminal'
            ],
            'productivity': [
                'word', 'excel', 'powerpoint', 'docs', 'sheets',
                'slides', 'outlook', 'slack', 'teams', 'zoom'
            ]
        }
        
        # Initialize the LLM for text analysis
        self.text_classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1  # CPU
        )
        
        # Create necessary directories
        self.setup_directories()
        
    def setup_directories(self):
        """Create necessary directories for storing data"""
        Path("screenshots").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
    
    def get_user_intentions(self):
        """Get user's intended activities through command line"""
        print("\nWhat activities do you plan to work on?")
        print("Examples:")
        print("- 'writing in Notepad and using Chrome for research'")
        print("- 'coding in Sublime Text and using Firefox for documentation'")
        print("- 'working on documents in Word and using the terminal'")
        intention = input("\nYour planned activities > ")
        self.intended_activities = self.parse_intentions(intention)
        logging.info(f"User intentions set: {self.intended_activities}")
        return intention
    
    def parse_intentions(self, intention):
        """Parse user's intention string into key activities"""
        intention = intention.lower()
        activities = []
        
        # Check for each category of applications
        for category, apps in self.work_applications.items():
            if any(app in intention for app in apps):
                activities.append(category)
        
        # Add generic work-related keywords
        work_keywords = ['research', 'documentation', 'writing', 'coding', 
                        'programming', 'studying', 'reading', 'working']
        
        if any(keyword in intention for keyword in work_keywords):
            activities.append('work')
            
        return list(set(activities))  # Remove duplicates
    
    def capture_screen(self):
        """Capture and save screenshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot = ImageGrab.grab()
        screenshot_path = f"screenshots/screen_{timestamp}.png"
        screenshot.save(screenshot_path)
        return screenshot_path
    
    def analyze_screenshot(self, screenshot_path):
        """Analyze screenshot content using computer vision"""
        img = cv2.imread(screenshot_path)
        
        # Convert to grayscale for text detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Basic analysis - looking for window patterns
        # In a real implementation, you would want to use more sophisticated
        # window title detection and OCR
        
        analysis_result = {
            'detected_apps': [],
            'has_text_editor': False,
            'has_browser': False,
            'has_terminal': False,
            'has_entertainment': False
        }
        
        # Simple detection based on common UI patterns
        # This is a placeholder - in real implementation you'd want proper
        # window detection and OCR
        if np.mean(gray) < 128:  # Dark theme common in text editors
            analysis_result['has_text_editor'] = True
        
        # You would add more sophisticated detection here
        
        return analysis_result
    
    def classify_content(self, analysis_result):
        """Classify screen content as work-related or entertainment"""
        # Check if any work-related applications are detected
        if (analysis_result['has_text_editor'] or 
            analysis_result['has_browser'] or 
            analysis_result['has_terminal']):
            
            # Check if intended activities match detected activities
            detected_categories = set()
            if analysis_result['has_text_editor']:
                detected_categories.add('text_editors')
            if analysis_result['has_browser']:
                detected_categories.add('browsers')
            if analysis_result['has_terminal']:
                detected_categories.add('terminals')
            
            # If any intended activity is detected, consider it work
            if any(activity in detected_categories for activity in self.intended_activities):
                return 'work'
        
        if analysis_result['has_entertainment']:
            return 'entertainment'
            
        return 'unknown'
    
    def compare_with_intentions(self, current_activity):
        """Compare current activity with stated intentions"""
        if current_activity == 'entertainment':
            return False
        return True
    
    def notify_user(self, message):
        """Show notification to user"""
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showwarning("Procrastination Alert", message)
        root.destroy()
    
    def log_activity(self, activity_type, details):
        """Log activity for later analysis"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'activity_type': activity_type,
            'details': details
        }
        self.log_data.append(log_entry)
        
        # Save to file
        with open('logs/activity_log.json', 'w') as f:
            json.dump(self.log_data, f, indent=2)
    
    def start_monitoring(self):
        """Start the monitoring process"""
        self.monitoring = True
        print("\nMonitoring started. The system will:")
        print("- Take screenshots every 5 minutes")
        print("- Analyze your activities")
        print("- Show warnings if you deviate from your planned activities")
        print("- Save activity logs for later analysis")
        print("\nPress Ctrl+C to stop monitoring and see your productivity report.")
        
        while self.monitoring:
            try:
                # Capture and analyze screen
                screenshot_path = self.capture_screen()
                analysis = self.analyze_screenshot(screenshot_path)
                activity_type = self.classify_content(analysis)
                
                # Check if activity matches intentions
                if not self.compare_with_intentions(activity_type):
                    self.notify_user("Warning: Current activity doesn't match your stated intentions!")
                
                # Log activity
                self.log_activity(activity_type, analysis)
                
                # Clean up screenshot
                os.remove(screenshot_path)
                
                # Wait for next interval
                time.sleep(self.screenshot_interval)
                
            except Exception as e:
                logging.error(f"Error during monitoring: {str(e)}")
    
    def stop_monitoring(self):
        """Stop the monitoring process"""
        self.monitoring = False
    
    def generate_report(self):
        """Generate productivity report"""
        work_time = 0
        entertainment_time = 0
        unknown_time = 0
        
        for entry in self.log_data:
            if entry['activity_type'] == 'work':
                work_time += self.screenshot_interval
            elif entry['activity_type'] == 'entertainment':
                entertainment_time += self.screenshot_interval
            else:
                unknown_time += self.screenshot_interval
        
        total_time = work_time + entertainment_time + unknown_time
        if total_time > 0:
            productivity_ratio = (work_time / total_time) * 100
        else:
            productivity_ratio = 0
        
        report = {
            'work_time_hours': work_time / 3600,
            'entertainment_time_hours': entertainment_time / 3600,
            'unknown_time_hours': unknown_time / 3600,
            'productivity_ratio': productivity_ratio
        }
        
        return report

def main():
    preventer = ProcrastinationPreventer()
    
    # Get user intentions
    preventer.get_user_intentions()
    
    try:
        # Start monitoring in a separate thread
        monitor_thread = threading.Thread(target=preventer.start_monitoring)
        monitor_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        preventer.stop_monitoring()
        
        # Generate and display report
        report = preventer.generate_report()
        print("\nProductivity Report:")
        print(f"Work time: {report['work_time_hours']:.2f} hours")
        print(f"Entertainment time: {report['entertainment_time_hours']:.2f} hours")
        print(f"Unknown time: {report['unknown_time_hours']:.2f} hours")
        print(f"Productivity ratio: {report['productivity_ratio']:.2f}%")

if __name__ == "__main__":
    main()s