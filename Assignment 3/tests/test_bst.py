import unittest
from ed_utils.decorators import number, visibility
from ed_utils.timeout import timeout

from bst import BinarySearchTree


class BSTTest(unittest.TestCase):

    @timeout()
    @number("1.1")
    def test_p1(self):
        BST = BinarySearchTree()
        BST[95] = 1
        BST[73] = 2
        BST[99] = 3
        BST[50] = 4
        BST[85] = 5
        BST[80] = 6

        minimal = BST.get_minimal(BST.root)
        self.assertEqual(minimal.key, 50)
        self.assertEqual(minimal.item, 4)

        minimal = BST.get_minimal(BST.root.right)
        self.assertEqual(minimal.key, 99)
        self.assertEqual(minimal.item, 3)

        successor = BST.get_successor(BST.root)
        self.assertEqual(successor.key, 99)
        self.assertEqual(successor.item, 3)

        successor = BST.get_successor(BST.root.left)
        self.assertEqual(successor.key, 80)
        self.assertEqual(successor.item, 6)

        successor = BST.get_successor(BST.root.left.right)
        self.assertEqual(successor, None)

    @timeout()
    @number("1.2")
    def test_p2(self):
        BST = BinarySearchTree()
        BST[95] = 1
        BST[73] = 2
        BST[99] = 3
        self.assertEqual(BST.root.subtree_size, 3)
        BST[50] = 4
        BST[85] = 5
        BST[80] = 6

        self.assertEqual(BST.root.subtree_size, 6)
        self.assertEqual(BST.root.left.subtree_size, 4)
        self.assertEqual(BST.root.right.subtree_size, 1)
        self.assertEqual(BST.root.left.left.subtree_size, 1)
        self.assertEqual(BST.root.left.right.subtree_size, 2)
        self.assertEqual(BST.root.left.right.left.subtree_size, 1)

    @timeout()
    @number("1.3")
    def test_p3(self):
        BST = BinarySearchTree()
        BST[95] = 1
        BST[73] = 2
        BST[99] = 3
        BST[50] = 4
        BST[85] = 5
        BST[80] = 6

        kth = BST.kth_smallest(3, BST.root)
        self.assertEqual(kth.key, 80)
        self.assertEqual(kth.item, 6)

        kth = BST.kth_smallest(2, BST.root.left.right)
        self.assertEqual(kth.key, 85)
        self.assertEqual(kth.item, 5)

        kth = BST.kth_smallest(5, BST.root)
        self.assertEqual(kth.key, 95)
        self.assertEqual(kth.item, 1)
