""" Calculate the degree with two given point """

import math


def check_angle(angle, degrees=False, vh_only=False):
    angles = [0, 45, 90, 75, 135, 180] if not vh_only else [0, 90, 180]
    angle = round(math.degrees(angle), 2) if not degrees else round(angle, 2)
    return True if angle in angles else False


def getAnglePoints(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    # print(ang)
    ang = ang + 360 if ang < 0 else ang
    if ang > 180:
        ang = 360 - ang
    return ang


def getAnglePoints_360(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    # print(ang)
    ang = ang + 360 if ang < 0 else ang
    return ang


def calc_degrees(pos1: tuple, pos2: tuple):
    if len(pos1) != 2 or len(pos2) != 2:
        raise ValueError("Point must be 2 dimensional")

    pos3 = (pos2[0], pos1[1])

    distance_1 = math.dist(pos1, pos2)
    distance_2 = distance_ptl(pos1, pos2, pos3)

    # print(distance_1, distance_2)

    degree = math.acos(distance_2/distance_1)

    return degree


def distance_ptl(pos1: tuple, pos2: tuple, pos3: tuple):
    """Calculate the distance from pos1 to line through pos2 to pos3
        pos1 x0,y0
        pos2 x1,y1
        pos3 x2,y2
     |(y2-y1)x0 - (x2-x1)y0 + x2y1 - y2x1|
     -------------------------------------
          √(y2-y1)**2 + (x2-x1)**2"""
    x = abs(((pos3[1]-pos2[1])*pos1[0]) - ((pos3[0]-pos2[0])*pos1[1]) + pos3[0]*pos2[1] - pos3[1]*pos2[0])
    y = ((pos3[1]-pos2[1])**2 + (pos3[0]-pos2[0])**2)**0.5

    return x/y if y != 0 else 0


def rotate_point(point, center, angle, counter_clockwise=False):
    """Rotates a point around a center by a given angle (in degrees)."""
    x, y = point
    cx, cy = center
    angle_rad = math.radians(angle)

    # Translate point to origin
    x -= cx
    y -= cy

    # Rotate point
    if counter_clockwise:
        rotated_x = x * math.cos(angle_rad) + y * math.sin(angle_rad)
        rotated_y = -x * math.sin(angle_rad) + y * math.cos(angle_rad)
    else:
        rotated_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
        rotated_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)

    # Translate point back to original position
    rotated_x += cx
    rotated_y += cy

    return rotated_x, rotated_y


if __name__ == "__main__":
    print(rotate_point((124.0, 490), (95, 461), 90, True))
    print(getAnglePoints_360((28, 394.0), (124.0, 490), rotate_point((95, 461),(124.0, 490), 90)))
    # print(np.cross(np.array([[0, 0], [1, 1]]), np.array([[3, 2], [4, 2]])))
