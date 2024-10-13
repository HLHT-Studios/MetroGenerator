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


def getTurnPoint(pos1: tuple, pos2: tuple, last_point=Station(0, 0), next_point=Station(0, 0),
                 use_last=False, use_next=False) -> tuple:
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

    result = (point[0], point[1])

    if use_last:
        mid_point = last_point.mid_point
        angle1 = round(degrees.getAnglePoints(mid_point, pos1, point), 2)
        angle2 = round(degrees.getAnglePoints(mid_point, pos1, _point), 2)

        # print(f"Pos: {pos1[0]}, {pos1[1]}")
        # print(f"Angles: {angle1}, {angle2}")
        # print(f"TPos: {mid_point}, {pos1}, {_point}")

        # if degrees.check_angle(angle1, True, True) or degrees.check_angle(angle2, True, True):
        #     point = point if angle1 > angle2 else _point
        #     print(angle1, angle2, last_point.name, "aaa")
        #     return point

        result = point if angle1 > angle2 else _point
        # print("Chose 1") if angle1 > angle2 else print("Chose 2")

    if use_next:
        angle_to_next = round(degrees.getAnglePoints(point, pos2, next_point.mid_point), 2)
        angle_to_next2 = round(degrees.getAnglePoints(_point, pos2, next_point.mid_point), 2)
        angle_this = round(degrees.getAnglePoints(pos1, point, pos2), 2)

        if angle_to_next >= 90 and angle_to_next2 >= 90:
            # print(angle_this, angle_to_next, angle_to_next2, last_point.name, "90")
            return result

        if angle_this + angle_to_next != angle_this + angle_to_next2:
            # print(angle_this, angle_to_next, angle_to_next2, last_point.name)

            if use_last:
                # print("last")
                angle_to_last = round(degrees.getAnglePoints(point, pos1, last_point.tuple), 2)
                angle_to_last2 = round(degrees.getAnglePoints(_point, pos1, last_point.tuple), 2)
                # print(angle_this, angle_to_last, angle_to_last2, last_point.name)
                result = point if min(angle_to_next, angle_this,
                                      angle_to_last) > min(angle_to_next2, angle_this, angle_to_last2) else _point
            else:
                result = point if angle_to_next + angle_this > angle_to_next2 + angle_this else _point
        else:
            # print(angle_this, angle_to_next, angle_to_next2, last_point.name, "bbb")
            result = point if min(angle_to_next, angle_this) > min(angle_to_next2, angle_this) else _point

    return result


if __name__ == '__main__':
    print(getTurnPoint((0, 0), (4, 2)))
