import math


def distance(a, b):
    return math.sqrt(
        (a.x - b.x) ** 2 +
        (a.y - b.y) ** 2
    )


def finger_angle(mcp, pip, dip):
    v1 = (
        mcp.x - pip.x,
        mcp.y - pip.y
    )

    v2 = (
        dip.x - pip.x,
        dip.y - pip.y
    )

    dot = (
        v1[0] * v2[0] +
        v1[1] * v2[1]
    )

    mag1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    mag2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

    cos_angle = dot / (mag1 * mag2)

    cos_angle = max(-1, min(1, cos_angle))

    return math.degrees(math.acos(cos_angle))