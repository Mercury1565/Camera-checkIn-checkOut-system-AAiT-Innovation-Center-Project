# Camera Attendance System with Face Recognition

This project consists of two main components:  
1. **Camera Application Module** - Responsible for handling the camera operations and attendance logic.  
2. **Face Recognition Server** - Runs the face recognition system as a separate service.

The system is designed for capturing attendance using face recognition in real-time.

---

## Features
- Real-time face detection and recognition.
- Attendance tracking using camera feeds.
- Modular structure separating camera logic and face recognition processing.

---

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Project Structure](#project-structure)
4. [Usage](#usage)
---

## Requirements
- Python 3.11 or higher
- `virtualenv` for environment isolation
- Libraries listed in the requirement texts
- Camera device for capturing video (for the Camera module)
- A server capable of running the face recognition model

---

## Installation

### Step 1: Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/camera-attendance-system.git
cd camera-attendance-system
```

### Step 2: Set Up Virtual Environments
For the Camera Application Module:

```bash
cd application
python3 -m venv app_venv
source app_venv/bin/activate
pip install -r app_requirements.txt
```

For the Face Recognition Server:

```bash
cd server
python3 -m venv server_venv
source server_venv/bin/activate 
pip install -r server_requirements.txt
```

Create a .env file in the application directory with the following info
```
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Project Structure

```
camera-attendance-system/
│
├── application/
│   ├── src/
|   |   ├── _init_.py
│   │   ├── app.py               # Main application logic
│   │   ├── camera.py            # Camera operation logic
│   │   ├── database.py          # Database connection and models
│   │   └── db_queries.py        # Define all the necessary database operations
│   ├── main.py                  # Entry point for Camera Application
|   ├── createTables.py          # Create the 'Users' and 'Attendace' tables
│   ├── app_requirements.txt     # Dependencies for Camera Application
|   └──.env
│
├── server/
│   ├── src/
|   |   ├── _init_.py
│   │   ├── face_recognition.py  # Core face recognition logic
│   │   ├── api.py               # API endpoints for recognition system
│   └── server_requirements.txt  # Dependencies for Recognition Server
│
└── README.md                    # Project documentation
```

## Usage

### Running the Face Recognition Server
1. Navigate to the server directory.
  ```bash
  cd server
  ```
2. Activate the server virtual environment:
  ```bash
  source server_venv/bin/activate  
  ```
3. Start the fast api server:
  ```bash
  uvicorn src.api:app --reload
  ```

### Running the Camera Application
1. Navigate to the application directory.
  ```bash
  cd application 
  ```
3. Activate the application virtual environment:
  ```bash
  source app_venv/bin/activate  
  ```
3. If you're running the app for the first time, execute the createTables.py file to create the necessary tables
  ```bash
  python3 createTables.py
  ```
4. Run the main application:
  ```bash
  python3 main.py
  ```

Upon completion, you will see the following command line interface
```
Enter command: [1 : register] [2 : check-in] [3 : check-out] [q : quit] 
```


