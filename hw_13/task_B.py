# B. Пересечение полуплоскостей

from decimal import Decimal

MAX_COORD = 10e9


class Point:
    def __init__(self, x, y):
        self.x = Decimal(x)
        self.y = Decimal(y)

    def __repr__(self):
        return f'{self.x:.10f} {self.y:.10f}'

    def insert_into_plane_equation(self, a, b, c):
        return a * self.x + b * self.y + c


class Vector:
    def __init__(self, point_1, point_2):
        self.x = point_2.x - point_1.x
        self.y = point_2.y - point_1.y

    def vect_mul(self, other):
        return self.x * other.y - self.y * other.x


class Line:
    def __init__(self, *args):
        if len(args) == 3:
            self.a, self.b, self.c = args
        elif len(args) == 2:
            point_1, point_2 = args
            self.a = point_1.y - point_2.y
            self.b = point_2.x - point_1.x
            self.c = point_1.x * point_2.y - point_2.x * point_1.y
        else:
            raise ValueError

    def solve_two_crossing_lines(self, other):
        d = self.a * other.b - other.a * self.b
        dx = self.b * other.c - other.b * self.c
        dy = self.c * other.a - other.c * self.a
        return Point(dx / d, dy / d)


class Polygon:
    def __init__(self, points):
        self.points = list(points)

    def get_area(self):
        min_x = min(point.x for point in self.points)
        min_y = min(point.y for point in self.points)
        anchor_point = Point(min_x, min_y)

        area = 0
        for idx in range(len(self.points)):
            jdx = (idx + 1) % len(self.points)
            area += Vector(self.points[idx], anchor_point).vect_mul(Vector(self.points[jdx], anchor_point)) / 2
        return area

    def cut(self, a, b, c):
        new_points = []

        for idx in range(len(self.points)):
            cur_point_value = self.points[idx].insert_into_plane_equation(a, b, c)
            if cur_point_value >= 0:
                new_points.append(self.points[idx])

            jdx = (idx + 1) % len(self.points)
            next_point_value = self.points[jdx].insert_into_plane_equation(a, b, c)
            if cur_point_value * next_point_value < 0:
                cross_point = Line(self.points[idx], self.points[jdx]).solve_two_crossing_lines(Line(a, b, c))
                new_points.append(cross_point)

        self.points = new_points


def main():
    polygon = Polygon([
        Point(-MAX_COORD, -MAX_COORD),
        Point(MAX_COORD, -MAX_COORD),
        Point(MAX_COORD, MAX_COORD),
        Point(-MAX_COORD, MAX_COORD),
    ])

    n_planes = int(input())
    for _ in range(n_planes):
        polygon.cut(*map(int, input().split()))

    print(f'{polygon.get_area():.10f}')


if __name__ == '__main__':
    main()
