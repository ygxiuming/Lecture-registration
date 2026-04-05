# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python script for automating lecture registration via a WeChat mini-program ("报名工具"). It handles login via token input, retrieves historical lectures, displays event information, and auto-submits registrations with pre-filled user data.

## Prerequisites & Installation

```bash
pip install -r requirements.txt
```

Dependencies (from requirements.txt):
- `opencv-python==4.6.0.66` - QR code display
- `requests==2.28.1` - HTTP requests
- `rich==12.6.0` - Console formatting

## Running the Application

```bash
python main.py
```

## Architecture

### File Structure

```
Lecture-registration/
├── main.py              # Main application with Login and Lecture classes
├── utils/
│   ├── config.py        # API endpoint configurations
│   └── method.py        # Reusable API helper functions
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation (Chinese)
```

### Core Components

**Login Class** (`main.py:32`)
- Handles authentication via WeChat mini-program token
- Token input and validation
- Retrieves user personal info and pre-filled data

**Lecture Class** (`main.py:217`)
- Extends Login class
- Manages lecture selection and registration
- Key methods:
  - `get_history_registration()` - Fetches user's lecture history
  - `get_registration_info(eid)` - Gets required registration fields
  - `submit_registration(token, eid, info)` - Submits registration
  - `generate_a_and_s(eid, token)` - Generates authentication signatures

**API Configuration** (`utils/config.py`)
- Contains all API endpoint configurations for the WeChat mini-program backend (api-xcx-qunsou.weiyoubot.cn)

### Authentication Flow

1. User provides WeChat mini-program token (captured via proxy tools like ProxyPin)
2. Token is validated against `/xcx/enroll/v1/userinfo`
3. User info and pre-filled data are retrieved
4. Registration uses signed requests with `_a` (signature) and `_s` (timestamp) parameters

### Pre-fill Data Matching

The script supports pre-filled information that matches lecture fields using subset matching:
- Pre-fill data stored in `extra_info` from user profile
- Fields are matched by checking if pre-fill keys are subsets of lecture field names
- Example: "姓名" pre-fill matches fields containing both "姓" and "名" characters

### Key API Endpoints

Base URL: `https://api-xcx-qunsou.weiyoubot.cn`
- `/xcx/enroll/v1/user/history` - Get user's lecture history
- `/xcx/enroll/v1/req_detail` - Get registration form fields
- `/xcx/enroll/v5/enroll` - Submit registration
- `/xcx/enroll/v1/extra_info` - Manage pre-fill data

## Development Notes

- Web-based token authentication has been deprecated; mini-program token capture is required
- The `_a` signature is generated using MD5 hash of lecture ID, timestamp, and token
- Registration supports delayed submission via "延迟时间" pre-fill field (value in milliseconds)
- The script uses rich console for formatted output and cv2 for QR code display (legacy, not currently used)
