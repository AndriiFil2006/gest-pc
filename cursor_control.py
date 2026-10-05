import os
import platform
import subprocess
import tkinter as tk
import threading
import time

SYSTEM = platform.system()

SMOOTHING_SPEED = 5

from config import (
    ACTIVE_LEFT,
    ACTIVE_RIGHT,
    ACTIVE_TOP,
    ACTIVE_BOTTOM,
)


def get_screen_size():
    root = tk.Tk()
    root.withdraw()

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()

    root.destroy()

    return width, height


SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()


current_x = SCREEN_WIDTH / 2
current_y = SCREEN_HEIGHT / 2

last_update_time = time.monotonic()

# -------------------------------
# Wayland cursor worker
# -------------------------------

latest_wayland_position = None
wayland_lock = threading.Lock()


def _wayland_cursor_worker():
    global latest_wayland_position

    while True:
        with wayland_lock:
            position = latest_wayland_position
            latest_wayland_position = None

        if position is None:
            # Don't burn 100% CPU
            threading.Event().wait(0.005)
            continue

        x, y = position

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


# Start worker only if we're on Linux Wayland
if (
    SYSTEM == "Linux"
    and os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"
):
    thread = threading.Thread(
        target=_wayland_cursor_worker,
        daemon=True
    )

    thread.start()


def move_cursor(x, y):
    global current_x, current_y, last_update_time

    # Keep landmark inside active region
    x = max(
        ACTIVE_LEFT,
        min(ACTIVE_RIGHT, x)
    )

    y = max(
        ACTIVE_TOP,
        min(ACTIVE_BOTTOM, y)
    )

    # Remap active region to 0.0 -> 1.0
    normalized_x = (
        x - ACTIVE_LEFT
    ) / (
        ACTIVE_RIGHT - ACTIVE_LEFT
    )

    normalized_y = (
        y - ACTIVE_TOP
    ) / (
        ACTIVE_BOTTOM - ACTIVE_TOP
    )

    # Map to screen
    target_x = int(
        (1 - normalized_x) * SCREEN_WIDTH
    )

    target_y = int(
        normalized_y * SCREEN_HEIGHT
    )

    target_x = max(
        0,
        min(SCREEN_WIDTH - 1, target_x)
    )

    target_y = max(
        0,
        min(SCREEN_HEIGHT - 1, target_y)
    )

    # Time-based smoothing
    now = time.monotonic()

    delta_time = now - last_update_time
    last_update_time = now

    alpha = 1 - pow(
        2.71828,
        -SMOOTHING_SPEED * delta_time
    )

    current_x += (
        target_x - current_x
    ) * alpha

    current_y += (
        target_y - current_y
    ) * alpha

    screen_x = int(current_x)
    screen_y = int(current_y)

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
        _move_linux_wayland(
            x,
            y
        )

    else:
        _move_linux_x11(
            x,
            y
        )


def _move_linux_wayland(x, y):
    global latest_wayland_position

    # Don't run ydotool here.
    # Just give the worker the newest position.

    with wayland_lock:
        latest_wayland_position = (
            x,
            y
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