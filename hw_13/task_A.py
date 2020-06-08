# A. Две окружности

from math import sqrt


class Circle:
    def __init__(self, center_x, center_y, radius):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

    def get_center_coords(self):
        return self.center_x, self.center_y


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __repr__(self):
        return f'{self.x:.10f} {self.y:.10f}'

    def get_squared_norm(self):
        return self.x ** 2 + self.y ** 2

    def get_norm(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def get_normed_vector(self):
        norm = self.get_norm()
        return Vector(self.x / norm, self.y / norm)

    def get_normal_vector(self):
        return Vector(-self.y, self.x)


def solve_circles(circle_1, circle_2):
    # define vectors for circles centers
    circle_1_vector = Vector(*circle_1.get_center_coords())
    circle_2_vector = Vector(*circle_2.get_center_coords())
    centers_vector = circle_2_vector - circle_1_vector
    squared_distance_between_centers = centers_vector.get_squared_norm()

    # identical circles
    if squared_distance_between_centers == 0 and circle_1.sq_radius == circle_2.sq_radius:
        print(3)
        return

    # no intersection
    if squared_distance_between_centers > (circle_1.sq_radius + circle_2.sq_radius) ** 2 \
            or squared_distance_between_centers < (circle_1.sq_radius - circle_2.sq_radius) ** 2:
        print(0)
        return

    # 1 outer point
    if squared_distance_between_centers == (circle_1.sq_radius + circle_2.sq_radius) ** 2:
        intersection_point = circle_1_vector + (
                circle_2_vector - circle_1_vector).get_normed_vector() * circle_1.sq_radius
        print(1)
        print(intersection_point)
        return

    # 1 inner point
    if squared_distance_between_centers == (circle_1.sq_radius - circle_2.sq_radius) ** 2:
        if circle_1.sq_radius > circle_2.sq_radius:
            direction_vector = centers_vector.get_normed_vector()
            step = circle_1.sq_radius
            intersection_point = circle_1_vector + direction_vector * step
        else:
            direction_vector = centers_vector.get_normed_vector() * -1
            step = circle_2.sq_radius
            intersection_point = circle_2_vector + direction_vector * step

        print(1)
        print(intersection_point)
        return

    # two points
    distance_between_centers = sqrt(squared_distance_between_centers)
    dist_h = (squared_distance_between_centers + circle_1.sq_radius ** 2 - circle_2.sq_radius ** 2) \
        / (2 * distance_between_centers)
    dist_hp = sqrt(circle_1.sq_radius ** 2 - dist_h ** 2)

    point_h = circle_1_vector + centers_vector.get_normed_vector() * dist_h
    normal_vector = centers_vector.get_normal_vector().get_normed_vector()

    print(2)
    print(point_h)
    print(f'{abs(dist_h):.10f} {dist_hp:.10f}')
    print(point_h + normal_vector * dist_hp)
    print(point_h - normal_vector * dist_hp)


def main():
    n_tests = int(input())
    for _ in range(n_tests):
        circle_1 = Circle(*map(int, input().split()))
        circle_2 = Circle(*map(int, input().split()))
        solve_circles(circle_1, circle_2)


if __name__ == '__main__':
    main()
