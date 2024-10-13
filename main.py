import basic.math as imath
from PIL import Image, ImageDraw, ImageFont
import random


class Station:

    def __init__(self, x, y, name="Station"):
        self.x = x
        self.y = y
        self.mid_point = (self.x, self.y)
        self.display_side = "NE"
        self.tuple = (x, y)
        self.name = name


def draw_station(draw: ImageDraw.Draw, station: Station):
    x = station.x
    y = station.y
    r = 15

    # draw black outline
    leftUpPoint = (x - r, y - r)
    rightDownPoint = (x + r, y + r)
    twoPointList = [leftUpPoint, rightDownPoint]
    draw.ellipse(twoPointList, fill=(0, 0, 0, 255))

    # draw white inner point
    r = r - 5
    leftUpPoint = (x - r, y - r)
    rightDownPoint = (x + r, y + r)
    twoPointList = [leftUpPoint, rightDownPoint]
    draw.ellipse(twoPointList, fill=(255, 255, 255, 255))


def draw_round(draw: ImageDraw.Draw, point: tuple, color):
    x = point[0]
    y = point[1]
    r = 10

    leftUpPoint = (x - r, y - r)
    rightDownPoint = (x + r, y + r)
    twoPointList = [leftUpPoint, rightDownPoint]
    draw.ellipse(twoPointList, fill=color)


def draw_text(image: Image, station: Station):
    text_img = Image.new('RGBA', (0, 0), (255, 255, 255, 0))
    length = int(ImageFont.truetype("basic\\font\\Minecraftia-Regular.ttf", 15).getlength(station.name)) + 1
    text_img = text_img.resize((length + 40, 25))
    draw = ImageDraw.Draw(text_img)
    draw.text((20, 0), station.name, font=ImageFont.truetype("basic\\font\\Minecraftia-Regular.ttf", 15),
              fill=(255, 255, 255, 255))
    direction = station.display_side
    # text_img.show()

    point = (0, -10)
    if direction in ["NE", "SW"]:
        text_img = text_img.rotate(45, expand=True)
        point = (0, (text_img.height - 10) * -1) if direction == "NE" else ((text_img.width - 10) * -1, -10)
    if direction in ["NW", "SE"]:
        text_img = text_img.rotate(315, expand=True)
        point = ((text_img.width - 10) * -1, (text_img.height - 10) * -1) if direction == "NW" else (-10, -10)

    if direction in ["S"]:
        text_img = text_img.rotate(90, expand=True)
        point = (-10, 0)

    if direction in ["N"]:
        text_img = text_img.rotate(270, expand=True)
        point = (0, (text_img.height - 10) * -1)

    if direction in ["W"]:
        point = (text_img.width * -1, -10)

    paste_pos = (station.x + point[0], station.y + point[1])

    image.paste(text_img, paste_pos, mask=text_img)


def find_text_angle(station: Station, station_b: Station):
    center = (station.x, station.y)
    pos = station.mid_point
    _pos = (round(imath.degrees.rotate_point(pos, center, 90)[0]),
            round(imath.degrees.rotate_point(pos, center, 90)[1]))

    # print(imath.degrees.getAnglePoints_360(_pos, center, station_b.mid_point))
    # print(_pos)
    if imath.degrees.getAnglePoints_360(_pos, center, station_b.mid_point) >= 15:
        _pos = _pos
    else:
        _pos = (round(imath.degrees.rotate_point(pos, center, 90, True)[0]),
                round(imath.degrees.rotate_point(pos, center, 90, True)[1]))
    direction = ""
    if _pos[0] == center[0]:
        direction += "N" if _pos[1] > pos[1] else "S"
    elif _pos[1] == center[1]:
        direction += "E" if _pos[0] > pos[0] else "W"
    else:
        dimension = imath.dimension.get_dimension(_pos, center, True)
        direction += "N" if dimension in [1, 2] else "S"
        direction += "E" if dimension in [1, 4] else "W"
    #     print(dimension)
    #
    # print(center, pos, _pos)
    # print(direction, station_b.mid_point)
    return direction


def generate(stations, color: tuple, loop=False) -> Image:
    image = Image.new("RGBA", (700, 700), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    points = []
    for i in range(5):
        points.append((random.randint(-200, 200), random.randint(-200, 200)))

    points = stations
    index = 0
    for i in points:
        if index + 1 > len(points) - 1:
            break
        # print(i.tuple, points[index+1].tuple)
        angle = imath.degrees.calc_degrees(i.tuple, points[index + 1].tuple)
        # print(math.degrees(angle))
        if imath.degrees.check_angle(angle):
            point = points[index + 1].tuple
        else:
            if index > 0:
                point = imath.getTurnPoint(i.tuple, points[index + 1].tuple, points[index - 1],
                                           use_last=True)
            else:
                point = imath.getTurnPoint(i.tuple, points[index + 1].tuple)
        # print(i.tuple, point)
        # print("\n")
        i.mid_point = point
        index += 1

    # look back to check each mid_point
    index = 0
    for i in points:
        if index + 1 > len(points) - 1:
            break
        angle = imath.degrees.calc_degrees(i.tuple, points[index + 1].tuple)
        if imath.degrees.check_angle(angle):
            point = points[index + 1].tuple
        else:
            if len(points) - 1 > index > 0:
                point = imath.getTurnPoint(i.tuple, points[index + 1].tuple, points[index - 1], points[index+1],
                                           use_last=True, use_next=True)
            elif index == 0:
                if loop:
                    point = imath.getTurnPoint(i.tuple, points[index + 1].tuple, points[-1], points[index+1],
                                               use_last=True, use_next=True)
                else:
                    point = imath.getTurnPoint(i.tuple, points[index + 1].tuple)
            else:
                if loop:
                    point = imath.getTurnPoint(i.tuple, points[index + 1].tuple, points[index - 1], points[0],
                                               use_last=True, use_next=True)
                else:
                    point = imath.getTurnPoint(i.tuple, points[index + 1].tuple, points[index - 1],
                                               use_last=True)
        i.mid_point = point
        index += 1

    index = 0
    for point in points:
        if index + 1 > len(points) - 1:
            break
        mid_point = point.mid_point
        draw.line((point.x, point.y, mid_point[0], mid_point[1]), fill=color, width=20)
        draw.line((mid_point[0], mid_point[1], points[index + 1].x, points[index + 1].y),
                  fill=color, width=20)
        draw_round(draw, mid_point, color)
        index += 1

    if loop:
        point1 = points[-1]
        point2 = points[0]
        point3 = points[-2]
        point4 = points[0]
        angle = imath.degrees.calc_degrees(point1.tuple, point2.tuple)
        if imath.degrees.check_angle(angle):
            point = point2.tuple
        else:
            point = imath.getTurnPoint(point1.tuple, point2.tuple, point3, point4,
                                       use_last=True, use_next=True)
        points[-1].mid_point = point
        draw.line((point1.tuple[0], point1.tuple[1], point[0], point[1]), fill=color, width=20)
        draw.line((point[0], point[1], point2.tuple[0], point2.tuple[1]),
                  fill=color, width=20)
        draw_round(draw, point, color)

    index = 0
    for point in points:
        draw_station(draw, point)
        if index == 0:
            point.display_side = find_text_angle(point, points[-1])
        else:
            point.display_side = find_text_angle(point, points[index - 1])
        draw_text(image, point)
        index += 1

    return image


if __name__ == '__main__':
    img = generate([Station(402, 590, name="Station1"), Station(566, 420, name="Station2"),
                    Station(421, 310, name="Station3"), Station(330, 240, name="Station4"),
                    Station(330, 324, name="Station5"), Station(226, 324, name="Station6"),
                    Station(272, 183, name="Station7"), Station(165, 118, name="Station8"),
                    Station(128, 238, name="Station9"), Station(128, 390, name="Station1 "),
                    Station(195, 561, name="Station11")],

                   (44, 178, 255, 255), True)

    img.show()
    img.save("template.png")
