import time

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from landmarks import Landmark, TRACKED_POINTS
from gestures import is_pointing
from cursor_control import move_cursor

from config import (
    ACTIVE_LEFT,
    ACTIVE_RIGHT,
    ACTIVE_TOP,
    ACTIVE_BOTTOM,
)

BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
VisionRunningMode = vision.RunningMode


options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
)


with HandLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(2)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    previous_time = time.time()

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp_ms = int(
            time.monotonic() * 1000
        )

        result = landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        height, width, _ = frame.shape

        active_left_px = int(ACTIVE_LEFT * width)
        active_right_px = int(ACTIVE_RIGHT * width)
        active_top_px = int(ACTIVE_TOP * height)
        active_bottom_px = int(ACTIVE_BOTTOM * height)

        cv2.rectangle(
            frame,
            (active_left_px, active_top_px),
            (active_right_px, active_bottom_px),
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "ACTIVE AREA",
            (active_left_px, active_top_px - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 0),
            2
        )

        if result.hand_landmarks:
            for hand in result.hand_landmarks:

                # Draw tracked landmarks
                for name, landmark_id in TRACKED_POINTS.items():
                    landmark = hand[landmark_id]

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    cv2.circle(
                        frame,
                        (x, y),
                        7,
                        (0, 0, 255),
                        -1
                    )

                    cv2.putText(
                        frame,
                        name,
                        (x + 10, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4,
                        (255, 255, 255),
                        1
                    )

                if is_pointing(hand):
                    cv2.putText(
                        frame,
                        "POINTING",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                    index_tip = hand[
                        Landmark.INDEX_FINGER_TIP
                    ]

                    # Move actual mouse cursor
                    move_cursor(
                        index_tip.x,
                        index_tip.y
                    )
                    # Draw fingertip marker
                    cursor_x = int(
                        index_tip.x * width
                    )

                    cursor_y = int(
                        index_tip.y * height
                    )

                    cv2.circle(
                        frame,
                        (cursor_x, cursor_y),
                        12,
                        (0, 255, 0),
                        2
                    )

        current_time = time.time()

        delta_time = current_time - previous_time

        if delta_time > 0:
            fps = 1 / delta_time
        else:
            fps = 0

        previous_time = current_time

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "MediaPipe Hands",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()