# Gesture PC

Gesture PC is a computer-vision project that uses a webcam and MediaPipe hand tracking to control the mouse cursor using hand gestures.

The program tracks hand landmarks in real time, detects when the user is pointing with their index finger, and maps the fingertip position from the webcam feed to the computer screen.

The goal of the project is to create a hands-free way to interact with a computer using natural hand gestures.

## Features

- Real-time webcam hand tracking
- MediaPipe Hand Landmarker detection
- Pointing gesture recognition
- Cursor movement using the index fingertip
- Cross-platform cursor-control support
- Linux Wayland support through `ydotool`
- Windows support through the Windows API
- macOS support through Quartz

Additional gestures such as clicking, dragging, scrolling, and other controls may be added later.

## How It Works

The basic pipeline is:

```text
Webcam
  ↓
OpenCV captures frame
  ↓
MediaPipe detects hand landmarks
  ↓
Gesture detection determines whether the user is pointing
  ↓
Index fingertip coordinates are extracted
  ↓
Coordinates are mapped to the computer screen
  ↓
Cursor moves to the corresponding position
```

MediaPipe provides normalized landmark coordinates ranging approximately from:

```text
x: 0.0 → 1.0
y: 0.0 → 1.0
```

These coordinates are converted into screen coordinates based on the user's monitor resolution.

## Project Structure

```text
gesture-pc/
├── main.py
├── gestures.py
├── hand_utils.py
├── landmarks.py
├── cursor_control.py
├── hand_landmarker.task
├── requirements.txt
└── README.md
```

### `main.py`

Handles:

- webcam capture
- MediaPipe processing
- hand landmark detection
- gesture detection
- cursor movement calls
- displaying the webcam feed

### `gesture_pc/vision/gestures.py`

Contains gesture-recognition logic such as:

```python
is_pointing(hand)
```

The pointing gesture currently requires:

- index finger extended
- middle finger folded
- ring finger folded
- pinky finger folded

### `gesture_pc/vision/hand_utils.py`

Contains reusable hand-analysis functions such as:

- calculating finger joint angles
- determining whether a finger is extended

### `gesture_pc/vision/landmarks.py`

Defines MediaPipe hand landmark IDs using an enum.

Example:

```python
Landmark.INDEX_FINGER_TIP
Landmark.INDEX_FINGER_PIP
Landmark.WRIST
```

### `gesture_pc/input/cursor_control.py`

Handles operating-system-specific cursor movement.

The project uses different cursor-control methods depending on the operating system:

```text
Windows
   ↓
Windows API

macOS
   ↓
Quartz

Linux X11
   ↓
PyAutoGUI

Linux Wayland
   ↓
ydotool
```

## Requirements

Recommended:

```text
Python 3.11+
```

The project currently works with MediaPipe's Tasks API rather than the older `mp.solutions` API.

## Python Setup

Clone the repository:

```bash
git clone <your-repository-url>
cd gesture-pc
```

Create a virtual environment:

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

## `requirements.txt`

A basic `requirements.txt` can contain:

```text
mediapipe==1.0.1
opencv-python

pyautogui; platform_system == "Linux" or platform_system == "Windows"
pyobjc-framework-Quartz; platform_system == "Darwin"
```

Platform-specific dependencies are only installed when needed.

## MediaPipe Model

This project uses the MediaPipe Hand Landmarker model.

The project expects the model file:

```text
hand_landmarker.task
```

to be located in the project root:

```text
gesture-pc/
├── main.py
├── hand_landmarker.task
└── ...
```

The MediaPipe configuration currently uses:

```python
HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode
