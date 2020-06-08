# E. Покрытие кругом

from math import sqrt
from random import shuffle


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Circle:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

    def print_circle(self):
        print(f'{self.center_x:.30f} {self.center_y:.30f}')
        print(f'{self.radius:.30f}')

    def check_inside_point(self, point):
        return (self.center_x - point.x) ** 2 + (self.center_y - point.y) ** 2 <= self.radius ** 2

    @classmethod
    def circle_from_two_points(cls, point_1, point_2):
        x = (point_1.x + point_2.x) / 2
        y = (point_1.y + point_2.y) / 2
        radius = sqrt((point_1.x - point_2.x) ** 2 + (point_1.y - point_2.y) ** 2) / 2
        return cls(x, y, radius)

    @classmethod
    def circle_from_three_points(cls, point_1, point_2, point_3):
        # https://ru.wikipedia.org/wiki/Описанная_окружность
        part_1 = point_2.x ** 2 + point_2.y ** 2 - point_3.x ** 2 - point_3.y ** 2
        part_2 = point_3.x ** 2 + point_3.y ** 2 - point_1.x ** 2 - point_1.y ** 2
        part_3 = point_1.x ** 2 + point_1.y ** 2 - point_2.x ** 2 - point_2.y ** 2
        denominator = point_1.x * (point_2.y - point_3.y) + point_2.x * (point_3.y - point_1.y) + point_3.x * (point_1.y - point_2.y)

        x = -(point_1.y * part_1 + point_2.y * part_2 + point_3.y * part_3) / (2 * denominator)
        y = (point_1.x * part_1 + point_2.x * part_2 + point_3.x * part_3) / (2 * denominator)

        radius = sqrt((point_1.x - x) ** 2 + (point_1.y - y) ** 2)
        return cls(x, y, radius)


def min_disc_with_two_points(points, border_point_1, border_point_2):
    min_circle = Circle.circle_from_two_points(border_point_1, border_point_2)
    for idx in range(len(points)):
        if not min_circle.check_inside_point(points[idx]):
            min_circle = Circle.circle_from_three_points(points[idx], border_point_1, border_point_2)

    return min_circle


def min_disc_with_one_point(points, border_point):
    min_circle = Circle.circle_from_two_points(points[0], border_point)
    for idx in range(1, len(points)):
        if not min_circle.check_inside_point(points[idx]):
            min_circle = min_disc_with_two_points(points[:idx], points[idx], border_point)

    return min_circle


def find_smallest_circle(points):
    min_circle = Circle.circle_from_two_points(points[0], points[1])

    for idx in range(2, len(points)):
        if not min_circle.check_inside_point(points[idx]):
            min_circle = min_disc_with_one_point(points[:idx], points[idx])

    return min_circle


def main():
    points_list = []

    n_points = int(input())
    for _ in range(n_points):
        points_list.append(Point(*map(int, input().split())))
    shuffle(points_list)

    min_circle = find_smallest_circle(points_list)
    min_circle.print_circle()


if __name__ == '__main__':
    main()
