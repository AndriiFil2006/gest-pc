import time

import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from landmarks import Landmark, TRACKED_POINTS
from hand_utils import finger_angle


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

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp_ms = int(time.monotonic() * 1000)

        result = landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        if result.hand_landmarks:
            height, width, _ = frame.shape

            for hand in result.hand_landmarks:

                # Draw the landmarks you're currently interested in
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

                # Calculate finger angles
                index_angle = finger_angle(
                    hand[Landmark.INDEX_FINGER_MCP],
                    hand[Landmark.INDEX_FINGER_PIP],
                    hand[Landmark.INDEX_FINGER_DIP]
                )

                middle_angle = finger_angle(
                    hand[Landmark.MIDDLE_FINGER_MCP],
                    hand[Landmark.MIDDLE_FINGER_PIP],
                    hand[Landmark.MIDDLE_FINGER_DIP]
                )

                ring_angle = finger_angle(
                    hand[Landmark.RING_FINGER_MCP],
                    hand[Landmark.RING_FINGER_PIP],
                    hand[Landmark.RING_FINGER_DIP]
                )

                pinky_angle = finger_angle(
                    hand[Landmark.PINKY_MCP],
                    hand[Landmark.PINKY_PIP],
                    hand[Landmark.PINKY_DIP]
                )

                # Temporary debugging
                print(
                    f"Index: {index_angle:.1f} | "
                    f"Middle: {middle_angle:.1f} | "
                    f"Ring: {ring_angle:.1f} | "
                    f"Pinky: {pinky_angle:.1f}"
                )

        cv2.imshow("MediaPipe Hands", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()