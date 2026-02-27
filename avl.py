# Name: Alec Ilstrup
# OSU Email: ilstrpa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 2/23/2026
# Description: Implementation of a self-balancing AVL Tree data structure that
#              inherits from BST. Maintains balance through rotations after
#               insertions and deletions to ensure O(log N) operations. Duplicate
#               values are not allowed. Each node tracks its parent pointer and
#               height for efficient rebalancing. Uses inorder successor for
#               removal of nodes with two children.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """AVL Tree class. Inherits from BST"""

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ---------------------------------------------------------------------- #

    def add(self, value: object) -> None:
        """
        adds a new value to the AVL tree while maintaining balance.
        duplicate values are not allowed
        """
        if self._root is None:
            self._root = AVLNode(value)
            return

        current = self._root

        while current is not None:
            if value == current.value:
                return

            elif value < current.value:
                if current.left is None:
                    new_node = AVLNode(value)
                    current.left = new_node
                    new_node.parent = current
                    break
                current = current.left

            else:
                if current.right is None:
                    new_node = AVLNode(value)
                    current.right = new_node
                    new_node.parent = current
                    break
                current = current.right


        while current is not None:
            self._rebalance(current)
            current = current.parent

    def remove(self, value: object) -> bool:
        """
        removes a value from the AVL tree while maintaining balance
        returns True if the value was removed, False otherwise
        """
        parent = None
        current = self._root

        while current is not None:
            if value == current.value:
                if current.left is None and current.right is None:
                    rebalance_start = parent
                    self._remove_no_subtrees(parent, current)

                elif current.left is None or current.right is None:
                    rebalance_start = parent
                    self._remove_one_subtree(parent, current)

                else:
                    rebalance_start = self._remove_two_subtrees(parent, current)

                while rebalance_start is not None:
                    self._rebalance(rebalance_start)
                    rebalance_start = rebalance_start.parent

                return True

            elif value < current.value:
                parent = current
                current = current.left
            else:
                parent = current
                current = current.right

        return False

    def _remove_no_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> None:
        """
        removes a node that has no children

        """
        if remove_parent is None:
            self._root = None

        elif remove_parent.left == remove_node:
            remove_parent.left = None

        else:
            remove_parent.right = None

    def _remove_one_subtree(self, remove_parent: AVLNode, remove_node: AVLNode) -> None:
        """
        removes a node that has one child. the child moves up to take the removed node's place.
        """
        if remove_node.left is not None:
            child = remove_node.left
        else:
            child = remove_node.right

        if remove_parent is None:
            self._root = child
            if child is not None:
                child.parent = None

        elif remove_parent.left == remove_node:
            remove_parent.left = child
            if child is not None:
                child.parent = remove_parent

        else:
            remove_parent.right = child
            if child is not None:
                child.parent = remove_parent

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        removes a node that has two children and finds the leftmost in right subtree
        """
        successor_parent = remove_node
        successor = remove_node.right

        while successor.left is not None:
            successor_parent = successor
            successor = successor.left

        remove_node.value = successor.value

        if successor.left is None and successor.right is None:
            self._remove_no_subtrees(successor_parent, successor)

        else:
            self._remove_one_subtree(successor_parent, successor)

        return successor_parent

    def _balance_factor(self, node: AVLNode) -> int:
        """
        calculates the balance factor of a node
        """
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)

        return left_height - right_height

    def _get_height(self, node: AVLNode) -> int:
        """
        returns the height of a node
        if the node is None, return -1
        """
        if node is None:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        rotates left on given node
        used when a node is right heavy
        """
        new_root = node.right

        node.right = new_root.left

        if new_root.left is not None:
            new_root.left.parent = node

        new_root.parent = node.parent

        if node.parent is None:
            self._root = new_root

        elif node == node.parent.left:
            node.parent.left = new_root

        else:
            node.parent.right = new_root

        new_root.left = node
        node.parent = new_root

        self._update_height(node)
        self._update_height(new_root)

        return new_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        rotates right on given node
        """

        new_root = node.left
        node.left = new_root.right

        if new_root.right is not None:
            new_root.right.parent = node

        new_root.parent = node.parent

        if node.parent is None:
            self._root = new_root
        elif node == node.parent.left:
            node.parent.left = new_root
        else:
            node.parent.right = new_root

        new_root.right = node
        node.parent = new_root

        self._update_height(node)
        self._update_height(new_root)

        return new_root

    def _rebalance(self, node: AVLNode) -> None:
        """
        checks if a node is unbalanced and performs appropriate rotation
        """

        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1:
            if self._balance_factor(node.left) < 0:
                self._rotate_left(node.left)

            self._rotate_right(node)

        elif balance < -1:
            if self._balance_factor(node.right) > 0:
                self._rotate_right(node.right)

            self._rotate_left(node)

    def _update_height(self, node: AVLNode) -> None:
        """
        recalculates and updates the height of a node based on its children
        height = 1 + max(left childs height, right childs height)
        """

        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)

        node.height = 1 + max(left_height, right_height)


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, 'DEL:', del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, 'DEL:', del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
