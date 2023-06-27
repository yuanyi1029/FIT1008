"""
Binary Search Tree ADT.
Defines a Binary Search Tree with linked nodes.
Each node contains a key and item as well as references to the children.
"""

from __future__ import annotations

__author__ = 'Brendon Taylor, modified by Alexey Ignatiev, further modified by Jackson Goerner'
__docformat__ = 'reStructuredText'

from typing import TypeVar, Generic
from node import TreeNode
import sys

# generic types
K = TypeVar('K')
I = TypeVar('I')
T = TypeVar('T')


class BinarySearchTree(Generic[K, I]):
    """ Basic binary search tree. """

    def __init__(self) -> None:
        """
        Initialises Binary Search Tree

        Complexity: O(1)
        """
        self.root: TreeNode | None = None
        self.length: int = 0

    def is_empty(self) -> bool:
        """
        Checks to see if the bst is empty

        Complexity: O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """
        Returns the number of nodes in the tree.

        Complexity: O(1)
        """
        return self.length

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the key is in the BST

        Complexity: O(__getitem__)
        where __getitem__ is the complexity of the __getitem__() method of the BinarySearchTree class
        """
        try:
            _ = self[key]

        except KeyError:
            return False

        else:
            return True

    def __getitem__(self, key: K) -> I:
        """
        Attempts to get an item in the tree, it uses the Key to attempt to find it

        Complexity: O(get_tree_node_by_key)
        where get_tree_node_by_key is the complexity of the get_tree_node_by_key() method of the BinarySearchTree class
        """
        return self.get_tree_node_by_key(key).item

    def get_tree_node_by_key(self, key: K) -> TreeNode:
        """
        Get the TreeNode in the BinarySearchTree

        Complexity: O(get_tree_node_by_key_aux) where get_tree_node_by_key_aux is the complexity of the
        get_tree_node_by_key_aux() method of the BinarySearchTree class
        """
        return self.get_tree_node_by_key_aux(self.root, key)

    def get_tree_node_by_key_aux(self, current: TreeNode, key: K) -> TreeNode:
        """
        Auxiliary function of get_tree_node_by_key() method of the BinarySearchTree class

        :raises KeyError: key is not found in the BinarySearchTree

        Arguments:
            -current: Root node of a current TreeNode
            -key: Key Type

        Best Complexity: O(CompK) when key is at the root
        Worst Complexity: O(CompK * D) when key is at the leaf
        where D is the depth of the tree, and CompK is the complexity of comparing the keys
        """
        if current is None:
            raise KeyError('Key not found: {0}'.format(key))

        elif key == current.key:
            return current

        elif key < current.key:
            return self.get_tree_node_by_key_aux(current.left, key)

        else:  # key > current.key
            return self.get_tree_node_by_key_aux(current.right, key)

        # Recursively traverses the child nodes of the BinarySearchTree starting from the current node, comparing the
        # provided key with the keys of the nodes. If a match is found, the corresponding TreeNode object is returned.
        # This process continues until a match is found or None is encountered, indicating that the key is not
        # present in the tree, which will raise a KeyError.

    def __setitem__(self, key: K, item: I) -> None:
        """
        Set a (key, item) pair in the BinarySearchTree

        Arguments:
            -key: Key Type
            -item: Item Type

        Complexity: O(insert_aux)
        where insert_aux is the complexity of the insert_aux() method of the BinarySearchTree class
        """
        self.root = self.insert_aux(self.root, key, item)

    def insert_aux(self, current: TreeNode, key: K, item: I) -> TreeNode:
        """
        Attempts to insert an item into the tree, it uses the Key to insert it

        Arguments:
            -current: Root node of a current TreeNode
            -key: Key Type
            -item: Item Type

        Best Complexity: O(CompK) inserts the item at the root.
        Worst Complexity: O(CompK * D) inserting at the bottom of the tree
        where D is the depth of the tree, and CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item=item)
            self.length += 1

        elif key < current.key:
            current.left = self.insert_aux(current.left, key, item)
            current.subtree_size += 1

        elif key > current.key:
            current.right = self.insert_aux(current.right, key, item)
            current.subtree_size += 1

        else:  # key == current.key
            raise ValueError('Inserting duplicate item')

        return current

        # Attempts to insert the key item pair into the BinarySearchTree by recursively traversing the tree based on
        # the provided key. If the current node is None, indicating an empty spot in the BinarySearchTree,
        # a new TreeNode is created with the given key and item, and the length of the tree is incremented.
        # Otherwise, the function determines the appropriate child node to traverse based on the key and recursively
        # calls itself on that child node. After each recursive call, the subtree size of the current node is updated
        # accordingly.

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, item) pair in the BinarySearchTree

        Arguments:
            -key: Key Type

        Complexity: O(delete_aux)
        where delete_aux is the complexity of the delete_aux() method of the BinarySearchTree class
        """
        self.root = self.delete_aux(self.root, key)

    def delete_aux(self, current: TreeNode, key: K) -> TreeNode | None:
        """
        Attempts to delete an item from the tree, it uses the Key to determine the node to delete.

        Arguments:
            -current: Root node of a current TreeNode
            -key: Key Type

        Best Complexity: O(CompK) when deleting root that has only one or no child
        Worst Complexity: O(CompK * D) when deleting leaf
        where D is the depth of the tree, and CompK is the complexity of comparing the keys
        """
        if current is None:
            raise ValueError('Deleting non-existent item')

        # If the current node is None, it means the key is not found in the tree, and a ValueError is raised.

        elif key < current.key:
            current.left = self.delete_aux(current.left, key)
            current.subtree_size -= 1

        # If the key is less than the current node's key, the method is recursively called on the left subtree.

        elif key > current.key:
            current.right = self.delete_aux(current.right, key)
            current.subtree_size -= 1

        # If the key is greater than the current node's key, the method is recursively called on the right subtree.

        else:
            if self.is_leaf(current):
                self.length -= 1
                return None

            elif current.left is None:
                self.length -= 1
                return current.right

            elif current.right is None:
                self.length -= 1
                return current.left

        # If the key is equal to the current node's key, the node is found and the deletion process begins.
        # -If the current node is a leaf node, it is deleted, and the tree length is decremented.
        # -If the current node has no left child, it is replaced by its right child, and the tree length is decremented.
        # -If the current node has no right child, it is replaced by its left child, and the tree length is decremented.
        # -If the current node has both left and right children, a successor node is found.

            # general case => find a successor
            successor: TreeNode = self.get_successor(current)
            current.key = successor.key
            current.item = successor.item
            current.subtree_size -= 1
            current.right = self.delete_aux(current.right, successor.key)

        # The successor is the node with the smallest key in the right subtree of the current node. The key and
        # item of the successor node are assigned to the current node, effectively replacing the current node
        # with the successor. The deletion process is then recursively performed on the right subtree to remove
        # the successor.

        return current

    def get_successor(self, current: TreeNode) -> TreeNode | None:
        """
        Get successor of the current node. It should be a child node having the smallest
        key among all the larger keys.

        Arguments:
            -current: Root node of a current subtree

        Best Complexity: O(1) when the current node has no larger key, no successor is available
        Worst Complexity: O(D) when the smallest key among the larger keys is at the bottom of the subtree.
        where D is the depth of the Binary Search Tree
        """
        if current.right is None:
            return None

        return self.get_minimal(current.right)

        # If the current node has no larger keys, this method will return None as there are no successors. If there
        # are successors, self.get_minimal() method is called to find the smallest key node starting from the larger
        # key node (current.right).

    def get_minimal(self, current: TreeNode) -> TreeNode:
        """
        Get a node having the smallest key in the current subtree.

        Arguments:
            -current: Root node of a current subtree

        Best Complexity: O(1) when the smallest key is at the root of the subtree.
        Worst Complexity: O(D) when the smallest key is at the bottom of the subtree.
        where D is the depth of the Binary Search Tree.
        """
        if current.left is None:
            return current

        return self.get_minimal(current.left)

        # The base case is when current.left is None, indicating that the Binary Search Tree's smaller keys
        # have been traversed down to the end. In this case, the current node which represents the smallest
        # key will be returned. If the base case is not met, the method will call itself where the current node
        # will now be the previous node's left child (smaller child).

    @staticmethod
    def is_leaf(current: TreeNode) -> bool:
        """
        Simple check whether the node is a leaf.

        Complexity: O(1)
        """
        return current.left is None and current.right is None

    def draw(self, to=sys.stdout):
        """
        Draw the tree in the terminal.

        Arguments:
            -to: Optional. The output stream where the tree will be drawn. Defaults to sys.stdout.

        Complexity: O(draw_aux)
        where draw_aux is the complexity of the draw_aux() method of the BinarySearchTree class
        """
        # get the nodes of the graph to draw recursively
        self.draw_aux(self.root, prefix='', final='', to=to)

    def draw_aux(self, current: TreeNode, prefix='', final='', to=sys.stdout) -> K:
        """
        Draw a node and then its children.

        Arguments:
            -current: The current node being drawn.
            -prefix: Optional. The prefix string to be added before the current node's representation.
            -final: Optional. The final string to be added after the current node's representation.
            -to: Optional. The output stream where the tree will be drawn. Defaults to sys.stdout.

        Complexity: O(n)
        where n is the number of nodes in the BinarySearchTree
        """
        if current is not None:
            real_prefix: str = prefix[:-2] + final
            print('{0}{1}'.format(real_prefix, str(current.key)), file=to)

            if current.left or current.right:
                self.draw_aux(current.left, prefix=prefix + '\u2551 ', final='\u255f\u2500', to=to)
                self.draw_aux(current.right, prefix=prefix + '  ', final='\u2559\u2500', to=to)

        else:
            real_prefix = prefix[:-2] + final
            print('{0}'.format(real_prefix), file=to)

    def kth_smallest(self, k: int, current: TreeNode) -> TreeNode | None:
        """
        Finds the kth smallest value by key in the subtree rooted at current.

        Arguments:
            -k: Integer that represents kth_smallest key
            -current: Root node of a current subtree

        Best Complexity: O(CompS) when kth_smallest key is at the root
        Worst Complexity: O(CompS * D) when kth_smallest key is at the leaf
        where D is the depth of the tree, and CompS is the complexity of comparing the size and k
        """
        if current is None or current.subtree_size < k:
            return None

        # If the current node is None or the subtree size is smaller than k, it means the kth smallest value cannot
        # be found in the subtree, and None is returned.

        if current.subtree_size == k and k == 1:
            return current

        # If the subtree size is k and k is 1, it means the current node is the kth smallest value, and the current
        # node is returned.

        left_size: int = current.left.subtree_size if current.left else 0

        # Calculate the number of nodes in the left subtree, considering that if there is no left subtree, it will be
        # an error when accessing current.left.subtree_size.

        if left_size + 1 == k:
            return current

        # If the number of nodes in the left subtree plus 1 is equal to k, it means the current node is the kth
        # smallest value, as it is bigger than the whole left subtree but smaller than the whole right subtree,
        # and the current node is returned.

        if left_size >= k:
            return self.kth_smallest(k, current.left)

        # If the number of nodes in the left subtree is greater than or equal to k, the kth smallest value is in the
        # left subtree, and the method is recursively called on the left subtree with the adjusted value of k.

        return self.kth_smallest(k - left_size - 1, current.right)

        # If the number of nodes in the left subtree plus 1 is less than k, the kth smallest value will be in the
        # right subtree. The value of k is adjusted by deducting the left size and root (which is 1), and the method
        # is recursively called on the right subtree with the adjusted value of k.
