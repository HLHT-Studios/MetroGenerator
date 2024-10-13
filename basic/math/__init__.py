import math

from basic.math import dimension, degrees
from main import Station


def getPos(pos1: tuple, pos2: tuple):
    direction = dimension.get_dimension(pos1, pos2)
    if direction == 1 or direction == 3:
        pos3 = (pos2[0] + 1, pos2[1] + 1)
    else:
        pos3 = (pos2[0] - 1, pos2[1] + 1)

    x = pos1[0]
    k, b = dimension.getLinearFunction(pos2, pos3)
    y = k * x + b
    point1 = (x, y)

    y2 = pos1[1]
    k2, b2 = dimension.getLinearFunction(pos2, pos3)
    x2 = (y2 - b2) / k2
    point2 = (x2, y2)

    return point1, point2


def getTurnPoint(pos1: tuple, pos2: tuple, last_point=Station(0, 0), use_last=False) -> tuple:
    point1, point2 = getPos(pos1, pos2)
    point3, point4 = getPos(pos2, pos1)

    if math.degrees(degrees.calc_degrees(pos1, pos2)) > 45:
        point = point1
        # _point = point3

    else:
        point = point2
        # _point = point4

    if math.degrees(degrees.calc_degrees(pos2, pos1)) > 45:
        _point = point3

    else:
        _point = point4

    if not use_last:
        return point
    else:
        mid_point = last_point.mid_point
        angle1 = round(degrees.getAnglePoints(mid_point, pos1, point), 2)
        angle2 = round(degrees.getAnglePoints(mid_point, pos1, _point), 2)

        # print(f"Pos: {pos1[0]}, {pos1[1]}")
        # print(f"Angles: {angle1}, {angle2}")
        # print(f"TPos: {mid_point}, {pos1}, {_point}")

        if degrees.check_angle(angle1, True) or degrees.check_angle(angle2, True):
            point = point if angle1 > angle2 else _point
            return point

        point = point if angle1 > angle2 else _point

        # print("Chose 1") if angle1 > angle2 else print("Chose 2")

        return point


if __name__ == '__main__':
    print(getTurnPoint((0, 0), (4, 2)))
