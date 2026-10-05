import math


def finger_angle(a, b, c):
    """
    Returns angle ABC in degrees using x, y, and z.
    b is the joint in the middle.
    """

    ba = (
        a.x - b.x,
        a.y - b.y,
        a.z - b.z
    )

    bc = (
        c.x - b.x,
        c.y - b.y,
        c.z - b.z
    )

    dot = (
        ba[0] * bc[0] +
        ba[1] * bc[1] +
        ba[2] * bc[2]
    )

    mag_ba = math.sqrt(
        ba[0] ** 2 +
        ba[1] ** 2 +
        ba[2] ** 2
    )

    mag_bc = math.sqrt(
        bc[0] ** 2 +
        bc[1] ** 2 +
        bc[2] ** 2
    )

    if mag_ba == 0 or mag_bc == 0:
        return 0

    cos_angle = dot / (mag_ba * mag_bc)

    cos_angle = max(-1, min(1, cos_angle))

    return math.degrees(math.acos(cos_angle))


def finger_extended(hand, mcp, pip, dip, tip):
    pip_angle = finger_angle(
        hand[mcp],
        hand[pip],
        hand[dip]
    )

    dip_angle = finger_angle(
        hand[pip],
        hand[dip],
        hand[tip]
    )

    return (
        pip_angle > 160
        and dip_angle > 160
    )