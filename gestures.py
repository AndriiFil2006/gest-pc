from landmarks import Landmark
from hand_utils import finger_extended


def is_pointing(hand):
    index_extended = finger_extended(
        hand,
        Landmark.INDEX_FINGER_MCP,
        Landmark.INDEX_FINGER_PIP,
        Landmark.INDEX_FINGER_DIP,
        Landmark.INDEX_FINGER_TIP
    )

    middle_extended = finger_extended(
        hand,
        Landmark.MIDDLE_FINGER_MCP,
        Landmark.MIDDLE_FINGER_PIP,
        Landmark.MIDDLE_FINGER_DIP,
        Landmark.MIDDLE_FINGER_TIP
    )

    ring_extended = finger_extended(
        hand,
        Landmark.RING_FINGER_MCP,
        Landmark.RING_FINGER_PIP,
        Landmark.RING_FINGER_DIP,
        Landmark.RING_FINGER_TIP
    )

    pinky_extended = finger_extended(
        hand,
        Landmark.PINKY_MCP,
        Landmark.PINKY_PIP,
        Landmark.PINKY_DIP,
        Landmark.PINKY_TIP
    )

    return (
        index_extended
        and not middle_extended
        and not ring_extended
        and not pinky_extended
    )