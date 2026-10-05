import os
import platform
import subprocess
import tkinter as tk


SYSTEM = platform.system()


def get_screen_size():
    root = tk.Tk()
    root.withdraw()

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    root.destroy()

    return width, height


SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()


def move_cursor(x, y):
    """
    x and y should be normalized MediaPipe coordinates:
    0.0 <= x <= 1.0
    0.0 <= y <= 1.0
    """

    # Mirror webcam horizontally
    screen_x = int((1 - x) * SCREEN_WIDTH)
    screen_y = int(y * SCREEN_HEIGHT)

    screen_x = max(0, min(SCREEN_WIDTH - 1, screen_x))
    screen_y = max(0, min(SCREEN_HEIGHT - 1, screen_y))

    if SYSTEM == "Windows":
        _move_windows(screen_x, screen_y)

    elif SYSTEM == "Darwin":
        _move_macos(screen_x, screen_y)

    elif SYSTEM == "Linux":
        _move_linux(screen_x, screen_y)

    else:
        raise RuntimeError(
            f"Unsupported operating system: {SYSTEM}"
        )


def _move_windows(x, y):
    import ctypes

    ctypes.windll.user32.SetCursorPos(
        x,
        y
    )


def _move_macos(x, y):
    try:
        import Quartz
    except ImportError:
        raise RuntimeError(
            "macOS requires pyobjc-framework-Quartz.\n"
            "Install it with:\n"
            "pip install pyobjc-framework-Quartz"
        )

    Quartz.CGWarpMouseCursorPosition(
        (x, y)
    )


def _move_linux(x, y):
    session_type = os.environ.get(
        "XDG_SESSION_TYPE",
        ""
    ).lower()

    if session_type == "wayland":
        _move_linux_wayland(x, y)

    else:
        _move_linux_x11(x, y)


def _move_linux_wayland(x, y):
    subprocess.run(
        [
            "ydotool",
            "mousemove",
            str(x),
            str(y),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _move_linux_x11(x, y):
    try:
        import pyautogui
    except ImportError:
        raise RuntimeError(
            "Linux X11 requires pyautogui.\n"
            "Install it with:\n"
            "pip install pyautogui"
        )

    pyautogui.moveTo(
        x,
        y,
        duration=0
    )