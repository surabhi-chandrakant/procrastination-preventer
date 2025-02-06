# Procrastination Preventer System

## Overview
The **Procrastination Preventer System** is an AI-powered tool that helps you stay focused on your intended activities by monitoring your screen and providing real-time alerts if you deviate from your planned tasks.

## Features
- Prompts the user for intended activities.
- Captures and analyzes screen activity every 5 minutes.
- Uses AI-based text classification to detect work-related activities.
- Sends warning notifications when non-work activities are detected.
- Logs all activity data and generates a productivity report.
- Allows customization of monitoring frequency and work-related keywords.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Virtual environment (recommended)
- Required Python packages

### Clone the Repository
```sh
git clone https://github.com/surabhi-chandrakant/procrastination-preventer.git
cd procrastination-preventer
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Usage
### Running the Program
To start monitoring, run:
```sh
python main.py
```

### What Happens When You Run the Program:
1. The program prompts for intended activities:
   ```
   What activities do you plan to work on? (e.g., 'coding in VS Code and using Chrome for documentation')
   >
   ```
   Example input:
   ```
   > I'm going to code in VS Code and use Chrome for documentation
   ```
2. The system will then:
   - Start monitoring the screen every 5 minutes.
   - Create necessary directories (`screenshots/` and `logs/` if they don’t exist).
   - Capture periodic screenshots.
   - Analyze the activities.
   - Show warning notifications if the detected activities don’t match your stated intentions.

### Stopping the Program
To stop monitoring, press `Ctrl+C` in the terminal.
Upon stopping, the program will display a final productivity report:
```
Stopping monitoring...

Productivity Report:
Work time: 1.50 hours
Entertainment time: 0.25 hours
Productivity ratio: 85.71%
```

### Important Notes
- **Directories Created:**
  - `screenshots/`: Temporary screenshots (deleted after analysis).
  - `logs/`: Stores `activity_log.json` with activity history.
- **Logs Available:**
  - `activity_log.txt`: General program logs.
  - `logs/activity_log.json`: Detailed activity data.
- The system **runs continuously** until stopped manually.
- Warning notifications appear as pop-ups for non-work activities.

## Customization
You can modify the following parameters in `main.py`:
- **`screenshot_interval`**: Change monitoring frequency (default: `300` seconds / `5` minutes).
- **`work_keywords`**: Modify work-related keywords in the `parse_intentions` method.

## Contributing
Feel free to fork this repository and submit pull requests to improve the system.



## Author
Developed by [surabhi c](https://github.com/surabhi-chandrakant).

