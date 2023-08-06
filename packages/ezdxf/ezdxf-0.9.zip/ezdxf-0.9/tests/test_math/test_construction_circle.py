# (c) 2009, Manfred Moitzi
# License: MIT License
import unittest
import math
from math import isclose
from ezdxf.math import is_close_points
from ezdxf.math.line import ConstructionRay
from ezdxf.math.circle import ConstructionCircle, Vec2

HALF_PI = math.pi / 2.


class TestConstructionCircle(unittest.TestCase):
    def test_init_circle(self):
        circle = ConstructionCircle((0., 0.), 5)
        point = circle.point_at(HALF_PI)
        self.assertAlmostEqual(point[0], 0., 3)
        self.assertAlmostEqual(point[1], 5., 3)
        point = circle.point_at(HALF_PI / 2)
        self.assertAlmostEqual(point[0], 3.5355, 3)
        self.assertAlmostEqual(point[1], 3.5355, 3)

    def test_within(self):
        circle = ConstructionCircle((0., 0.), 5)
        p1 = (3., 2.)
        p2 = (4., 5.)
        self.assertTrue(circle.inside(p1))
        self.assertFalse(circle.inside(p2))

    def test_tangent(self):
        circle = ConstructionCircle((0., 0.), 5.)
        tangent = circle.tangent(HALF_PI / 2)
        self.assertAlmostEqual(tangent._slope, -1, 4)
        tangent = circle.tangent(-HALF_PI / 2)
        self.assertAlmostEqual(tangent._slope, 1, 4)
        tangent = circle.tangent(0)
        self.assertTrue(tangent._is_vertical)
        tangent = circle.tangent(HALF_PI)
        self.assertTrue(tangent._is_horizontal)

    def test_intersect_ray_pass(self):
        circle = ConstructionCircle((10., 10.), 3)
        ray1_hor = ConstructionRay((10., 15.), angle=0)
        ray2_hor = ConstructionRay((10., 5.), angle=0)
        ray1_vert = ConstructionRay((5., 10.), angle=HALF_PI)
        ray2_vert = ConstructionRay((15., 10.), angle=-HALF_PI)
        ray3 = ConstructionRay((13.24, 14.95), angle=0.3992)
        self.assertFalse(circle.intersect_ray(ray1_hor))
        self.assertFalse(circle.intersect_ray(ray2_hor))
        self.assertFalse(circle.intersect_ray(ray1_vert))
        self.assertFalse(circle.intersect_ray(ray2_vert))
        self.assertFalse(circle.intersect_ray(ray3))

    def test_intersect_ray_touch(self):
        def test_touch(testnum, x, y, _angle, abs_tol=1e-6):
            result = True
            ray = ConstructionRay((x, y), angle=_angle)
            points = circle.intersect_ray(ray, abs_tol=abs_tol)
            if len(points) != 1:
                result = False
            else:
                point = points[0]
                # print ("{0}: x= {1:.{places}f} y= {2:.{places}f} : x'= {3:.{places}f} y' = {4:.{places}f}".format(testnum, x, y, point[0], point[1], places=places))
                if not isclose(point[0], x, abs_tol=abs_tol):
                    result = False
                if not isclose(point[1], y, abs_tol=abs_tol):
                    result = False
            return result

        circle = ConstructionCircle((10., 10.), 3)
        self.assertTrue(test_touch(1, 10., 13., 0))
        self.assertTrue(test_touch(2, 10., 7., 0))
        self.assertTrue(test_touch(3, 7., 10., HALF_PI))
        self.assertTrue(test_touch(4, 13., 10., -HALF_PI))
        self.assertTrue(test_touch(5, 8.8341, 12.7642, 0.3991568, abs_tol=1e-4))

    def test_intersect_ray_intersect(self):
        circle = ConstructionCircle((10., 10.), 3)
        ray_vert = ConstructionRay((8.5, 10.), angle=HALF_PI)
        cross_points = circle.intersect_ray(ray_vert)
        self.assertEqual(len(cross_points), 2)
        p1, p2 = cross_points
        if p1[1] > p2[1]: p1, p2 = p2, p1
        self.assertTrue(is_close_points(p1, (8.5, 7.4019), abs_tol=1e-4))
        self.assertTrue(is_close_points(p2, (8.5, 12.5981), abs_tol=1e-4))

        ray_hor = ConstructionRay((10, 8.5), angle=0.)
        cross_points = circle.intersect_ray(ray_hor)
        self.assertEqual(len(cross_points), 2)
        p1, p2 = cross_points
        if p1[0] > p2[0]: p1, p2 = p2, p1
        self.assertTrue(is_close_points(p1, (7.4019, 8.5), abs_tol=1e-4))
        self.assertTrue(is_close_points(p2, (12.5981, 8.5), abs_tol=1e-4))

        ray_slope = ConstructionRay((5, 5), (16, 12))
        cross_points = circle.intersect_ray(ray_slope)
        self.assertEqual(len(cross_points), 2)
        p1, p2 = cross_points
        if p1[0] > p2[0]: p1, p2 = p2, p1
        self.assertTrue(is_close_points(p1, (8.64840, 7.3217), abs_tol=1e-4))
        self.assertTrue(is_close_points(p2, (12.9986, 10.0900), abs_tol=1e-4))

        # ray with slope through midpoint
        ray_slope = ConstructionRay((10, 10), angle=HALF_PI / 2)
        cross_points = circle.intersect_ray(ray_slope)
        self.assertEqual(len(cross_points), 2)
        p1, p2 = cross_points
        if p1[0] > p2[0]: p1, p2 = p2, p1
        # print (p1[0], p1[1], p2[0], p2[1])
        self.assertTrue(is_close_points(p1, (7.8787, 7.8787), abs_tol=1e-4))
        self.assertTrue(is_close_points(p2, (12.1213, 12.1213), abs_tol=1e-4))

        # horizontal ray through midpoint
        ray_hor = ConstructionRay((10, 10), angle=0)
        cross_points = circle.intersect_ray(ray_hor)
        self.assertEqual(len(cross_points), 2)
        p1, p2 = cross_points
        if p1[0] > p2[0]: p1, p2 = p2, p1
        # print (p1[0], p1[1], p2[0], p2[1])
        self.assertTrue(is_close_points(p1, (7, 10), abs_tol=1e-5))
        self.assertTrue(is_close_points(p2, (13, 10), abs_tol=1e-5))

        # vertical ray through midpoint
        ray_vert = ConstructionRay((10, 10), angle=HALF_PI)
        cross_points = circle.intersect_ray(ray_vert)
        self.assertEqual(len(cross_points), 2)
        p1, p2 = cross_points
        if p1[1] > p2[1]: p1, p2 = p2, p1
        # print (p1[0], p1[1], p2[0], p2[1])
        self.assertTrue(is_close_points(p1, (10, 7), abs_tol=1e-5))
        self.assertTrue(is_close_points(p2, (10, 13), abs_tol=1e-5))

    def test_intersect_circle_pass(self):
        M1 = (30, 30)
        M2 = (40, 40)
        M3 = (30.3, 30.3)
        circle1 = ConstructionCircle(M1, 5)
        circle2 = ConstructionCircle(M1, 3)
        circle3 = ConstructionCircle(M2, 3)
        circle4 = ConstructionCircle(M3, 3)

        cross_points = circle1.intersect_circle(circle2)
        self.assertFalse(cross_points)
        cross_points = circle2.intersect_circle(circle3)
        self.assertFalse(cross_points)
        cross_points = circle1.intersect_circle(circle4)
        self.assertFalse(cross_points)

    def test_intersect_circle_touch(self):
        def check_touch(m, t, abs_tol=1e-9):
            circle2 = ConstructionCircle(m, 1.5)
            points = circle1.intersect_circle(circle2, 4)
            self.assertEqual(len(points), 1)
            return is_close_points(points[0], Vec2(t), abs_tol=abs_tol)

        circle1 = ConstructionCircle((20, 20), 5)

        self.assertTrue(check_touch((26.5, 20.), (25., 20.)))
        self.assertTrue(check_touch((20., 26.5), (20., 25.)))
        self.assertTrue(check_touch((13.5, 20.), (15., 20.)))
        self.assertTrue(check_touch((20., 13.5), (20., 15.)))
        self.assertTrue(check_touch((14.9339, 15.9276), (16.1030, 16.8674), abs_tol=1e-4))

        self.assertTrue(check_touch((23.5, 20.), (25., 20.)))
        self.assertTrue(check_touch((20., 23.5), (20., 25.)))
        self.assertTrue(check_touch((16.5, 20.), (15., 20.)))
        self.assertTrue(check_touch((20., 16.5), (20., 15.)))
        self.assertTrue(check_touch((17.2721, 17.8071), (16.1030, 16.8673), abs_tol=1e-4))

    def test_intersect_circle_intersect(self):
        def check_intersection(m, p1, p2, abs_tol=1e-4):
            p1 = Vec2(p1)
            p2 = Vec2(p2)
            circle2 = ConstructionCircle(m, 1.5)
            points = circle1.intersect_circle(circle2, abs_tol=abs_tol)
            self.assertEqual(len(points), 2)
            a, b = points

            result1 = is_close_points(a, p1, abs_tol=abs_tol) and is_close_points(b, p2, abs_tol=abs_tol)
            result2 = is_close_points(a, p2, abs_tol=abs_tol) and is_close_points(b, p1, abs_tol=abs_tol)
            return result1 or result2

        circle1 = ConstructionCircle((40, 20), 5)
        self.assertTrue(check_intersection((46., 20.), (44.8958, 21.0153), (44.8958, 18.9847)))
        self.assertTrue(check_intersection((44., 20.), (44.8438, 21.2402), (44.8438, 18.7598)))
        self.assertTrue(check_intersection((40., 26.), (38.9847, 24.8958), (41.0153, 24.8958)))
        self.assertTrue(check_intersection((40., 24.), (38.7598, 24.8438), (41.2402, 24.8438)))
        self.assertTrue(check_intersection((34., 20.), (35.1042, 18.9847), (35.1042, 21.0153)))
        # self.assertTrue(check_intersection( (36.,20.),  (35.1563, 18.7598),  (35.1563, 21.2402)))
        self.assertTrue(check_intersection((40., 14.), (38.9847, 15.1042), (41.0153, 15.1042)))
        self.assertTrue(check_intersection((40., 14.), (38.9847, 15.1042), (41.0153, 15.1042)))
        self.assertTrue(check_intersection((36.8824, 17.4939), (35.4478, 17.9319), (37.0018, 15.9987)))
        self.assertTrue(check_intersection((35.3236, 16.2408), (35.5481, 17.7239), (36.8203, 16.1413)))

    def test_create_3P(self):
        p1 = (3., 3.)
        p2 = (5., 7.)
        p3 = (12., 5.)
        circle = ConstructionCircle.from_3p(p1, p2, p3)
        self.assertAlmostEqual(circle.center[0], 7.6875, 4)
        self.assertAlmostEqual(circle.center[1], 3.15625, 4)
        self.assertAlmostEqual(circle.radius, 4.6901, 4)
