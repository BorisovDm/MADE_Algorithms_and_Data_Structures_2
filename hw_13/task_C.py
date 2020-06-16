# C. Площади

MAX_COORD = 10e4
MIN_AREA = 1e-8


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
        elif len(args) == 4:
            x_1, y_1, x_2, y_2 = args
            self.a = y_1 - y_2
            self.b = x_2 - x_1
            self.c = x_1 * y_2 - x_2 * y_1
        else:
            raise ValueError

    def __mul__(self, other):
        return Line(self.a * other, self.b * other, self.c * other)

    def get_params(self):
        return self.a, self.b, self.c

    def solve_two_crossing_lines(self, other):
        d = self.a * other.b - other.a * self.b
        dx = self.b * other.c - other.b * self.c
        dy = self.c * other.a - other.c * self.a
        return Point(dx / d, dy / d)


class Polygon:
    def __init__(self, points):
        self.points = list(points)

    def get_area(self):
        if len(self.points) == 0:
            return 0

        min_x = min(point.x for point in self.points)
        min_y = min(point.y for point in self.points)
        anchor_point = Point(min_x, min_y)

        area = 0
        for idx in range(len(self.points)):
            jdx = (idx + 1) % len(self.points)
            area += Vector(self.points[idx], anchor_point).vect_mul(Vector(self.points[jdx], anchor_point)) / 2
        return area

    def cut(self, a, b, c):
        pos_points = []
        neg_points = []

        for idx in range(len(self.points)):
            cur_point_value = self.points[idx].insert_into_plane_equation(a, b, c)
            if cur_point_value >= 0:
                pos_points.append(self.points[idx])
            if cur_point_value <= 0:
                neg_points.append(self.points[idx])

            jdx = (idx + 1) % len(self.points)
            next_point_value = self.points[jdx].insert_into_plane_equation(a, b, c)
            if cur_point_value * next_point_value < 0:
                cross_point = Line(self.points[idx], self.points[jdx]).solve_two_crossing_lines(Line(a, b, c))
                pos_points.append(cross_point)
                neg_points.append(cross_point)

        result = []
        if len(pos_points) > 0:
            result.append(Polygon(pos_points))
        if len(neg_points) > 0:
            result.append(Polygon(neg_points))

        return result


def cut_polygons(polygons, plane):
    result = []
    for polygon in polygons:
        result.extend(polygon.cut(*plane.get_params()))
    result = [polygon for polygon in result if polygon.get_area() >= MIN_AREA]
    return result


def main():
    initial_polygon = Polygon([
        Point(-MAX_COORD, -MAX_COORD),
        Point(MAX_COORD, -MAX_COORD),
        Point(MAX_COORD, MAX_COORD),
        Point(-MAX_COORD, MAX_COORD),
    ])
    polygons = [initial_polygon]

    n_planes = int(input())
    for _ in range(n_planes):
        line = Line(*map(int, input().split()))
        polygons = cut_polygons(polygons, line)

    finite_areas = []
    for polygon in polygons:
        for point in polygon.points:
            if abs(abs(point.x) - MAX_COORD) < 1e-6 or abs(abs(point.y) - MAX_COORD) < 1e-6:
                break
        else:
            finite_areas.append(polygon.get_area())
    finite_areas.sort()

    print(len(finite_areas))
    for area in finite_areas:
        print(f'{area:.10f}')


if __name__ == '__main__':
    main()
