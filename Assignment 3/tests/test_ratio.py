import random
import unittest
from ed_utils.decorators import number, visibility
from ed_utils.timeout import timeout

from ratio import Percentiles


class RatioTest(unittest.TestCase):

    @timeout()
    @number("2.1")
    def test_example(self):
        random.seed(1293810293)
        p = Percentiles()
        points = [4, 9, 14, 15, 16, 82, 87, 91, 92, 99]
        random.shuffle(points)
        for point in points:
            p.add_point(point)
        res = p.ratio(13, 10)
        self.assertSetEqual(set(res), {14, 15, 16, 82, 87, 91, 92})

        res = p.ratio(0, 42)
        self.assertSetEqual(set(res), {4, 9, 14, 15, 16})

    @timeout()
    @number("2.2")
    def test_removal(self):
        random.seed(2938742)
        p = Percentiles()
        points = [4, 9, 14, 15, 16, 82, 87, 91, 92, 99]
        random.shuffle(points)
        for point in points:
            p.add_point(point)
        p.remove_point(4)
        p.remove_point(92)

        res = p.ratio(13, 10)
        self.assertSetEqual(set(res), {15, 16, 82, 87, 91})

        p.remove_point(82)
        res = p.ratio(13, 10)
        self.assertSetEqual(set(res), {14, 15, 16, 87, 91})
