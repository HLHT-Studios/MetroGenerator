""" Calculate which dimension is pos1 in relatively to pos2 """


def getLinearFunction(point1, point2):
    """point1 (tuple), point2(tuple)"""
    x1 = point1[0]
    x2 = point2[0]
    y1 = point1[1]
    y2 = point2[1]
    k = (y1 - y2) / (x1 - x2)
    b = float(y1 - (k * x1))
    return k, b


def get_dimension(pos1: tuple, pos2: tuple, reverse=False):
    """ Calculate which dimension is pos1 in relatively to pos2 """
    if len(pos1) != 2 or len(pos2) != 2:
        raise ValueError("Point must be 2 dimensional")
    if pos1[0] == pos2[0] or pos1[1] == pos2[1]:
        raise ValueError("pos1 and pos2 are on the same line!")

    _x = pos1[0] - pos2[0]
    _y = pos1[1] - pos2[1]
    if reverse:
        _y = _y*-1
    quadrants = 1
    x = True
    y = True
    if _x < 0:
        x = False
        quadrants += 1
    if _y < 0:
        y = False

        quadrants += 3 if x else 1

    # print(_x)

    return quadrants
