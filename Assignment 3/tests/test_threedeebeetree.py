import unittest
from ed_utils.decorators import number, visibility
from ed_utils.timeout import timeout

from threedeebeetree import ThreeDeeBeeTree


class TestThreeDeeBeeTree(unittest.TestCase):
    TESTING_POINTS = [
        (6, -1, -17),
        (-11, 4, -16),
        (5, 5, 7),
        (-16, 2, -6),
        (10, -20, 1),
        (-14, 18, -4),
        (-18, 7, 5),
        (16, 0, -14),
        (-6, -14, 12),
        (4, 6, 19)
    ]

    @timeout()
    @number("3.1")
    def test_positions(self):
        tdbt = ThreeDeeBeeTree()
        for i, point in enumerate(self.TESTING_POINTS):
            tdbt[point] = i

        child = tdbt.root.get_child_for_key((-11, 4, -16))
        self.assertEqual(child.key, (-11, 4, -16))

        subchild = child.get_child_for_key((-18, 7, 5))
        self.assertEqual(subchild.key, (-14, 18, -4))

        other_subchild = child.get_child_for_key((3, 10, 20))
        self.assertEqual(other_subchild.key, (5, 5, 7))

        empty = tdbt.root.get_child_for_key((-6, 3, -20))
        self.assertEqual(empty, None)

    @timeout()
    @number("3.2")
    def test_subtree_sizes(self):
        tdbt = ThreeDeeBeeTree()
        for i, point in enumerate(self.TESTING_POINTS):
            tdbt[point] = i

        child = tdbt.root.get_child_for_key((-11, 4, -16))
        subchild = child.get_child_for_key((-18, 7, 5))
        other_subchild = child.get_child_for_key((3, 10, 20))

        self.assertEqual(tdbt.root.subtree_size, 10)
        self.assertEqual(child.subtree_size, 6)
        self.assertEqual(subchild.subtree_size, 2)
        self.assertEqual(other_subchild.subtree_size, 2)

    @timeout()
    @number("3.3")
    def test_get_node(self):
        tdbt = ThreeDeeBeeTree()
        for i, point in enumerate(self.TESTING_POINTS):
            tdbt[point] = i

        self.assertEqual(tdbt.get_tree_node_by_key((16, 0, -14)).item, 7)
        self.assertEqual(tdbt.get_tree_node_by_key((6, -1, -17)).item, 0)
