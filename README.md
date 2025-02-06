# procrastination-preventer
# Procrastination Preventer System

## Overview
The Procrastination Preventer is a system designed to help users stay on track with their intended activities. It uses computer vision and an AI model to monitor screen activity, classify user behavior, and provide real-time alerts if the user deviates from their planned work.

## Features
- Captures periodic screenshots of the user's screen.
- Uses AI-based text classification to detect work-related activities.
- Alerts the user if detected activities do not match their stated intentions.
- Logs all activity for productivity analysis.
- Generates a productivity report.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Git

### Clone the Repository
```sh
git clone https://github.com/your-username/procrastination-preventer.git
cd procrastination-preventer
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

## Usage

### Set Up User Intentions
Run the script and input your planned activities:
```sh
python main.py
```

The system will:
1. Monitor screen activity.
2. Classify detected applications.
3. Alert you if you deviate from intended work.
4. Log all activity and generate a productivity report.

### Stop Monitoring
Press `Ctrl + C` to stop the monitoring process. A productivity report will be displayed.

## File Structure
```
procrastination-preventer/
│── main.py               # Main script
│── requirements.txt      # Dependencies
│── screenshots/         # Stores screenshots (auto-generated)
│── logs/               # Activity logs (auto-generated)
│── README.md            # Project documentation
```

## Dependencies
- `torch`
- `transformers`
- `opencv-python`
- `numpy`
- `pillow`
- `tkinter`

To install manually:
```sh
pip install torch transformers opencv-python numpy pillow
```

## Contribution
Feel free to fork the repo, submit pull requests, or raise issues for feature suggestions.

## License
This project is licensed under the MIT License.

