# Name: Alec Ilstrup
# OSU Email: ilstrpa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 2/23/2026
# Description: Implementation of a Binary Search Tree (BST) data structure.
#               Includes methods for adding, removing, and searching for values,
#               as well as traversal and utility operations. Duplicate values are
#               allowed and placed in the right subtree. Removal uses the inorder
#               successor (leftmost node in right subtree) for nodes with two children.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value  # to store node's data
        self.left = None    # pointer to root of left subtree
        self.right = None   # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """Binary Search Tree class"""

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    def print_tree(self):
        """
        Prints the tree using the print_subtree function.

        This method is intended to assist in visualizing the structure of the
        tree. You are encouraged to add this method to the tests in the Basic
        Testing section of the starter code or your own tests as needed.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.get_root():
            self._print_subtree(self.get_root())
        else:
            print('(empty tree)')

    def _print_subtree(self, node, prefix: str = '', branch: str = ''):
        """
        Recursively prints the subtree rooted at this node.

        This is intended as a 'helper' method to assist in visualizing the
        structure of the tree.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """

        def add_junction(string):
            """
            Adds a 'junction marker' to a string prefix as a connecting line
            to visually represent branches between nodes in a subtree

            Helper method for _print_subtree() to aid in tree formatting

            DO NOT CHANGE THIS METHOD IN ANY WAY
            """
            if len(string) < 2 or branch == '':
                return string
            junction = '|' if string[-2] == '|' else '`'
            return string[:-2] + junction + '-'

        if not node:
            print(add_junction(prefix) + branch + "None")
            return

        if len(prefix) > 2 * 16:
            print(add_junction(prefix) + branch + "(tree continues)")
            return

        if node.left or node.right:
            postfix = ' (root)' if branch == '' else ''
            print(add_junction(prefix) + branch + str(node.value) + postfix)
            self._print_subtree(node.right, prefix + '| ', 'R: ')
            self._print_subtree(node.left, prefix + '  ', 'L: ')
        else:
            print(add_junction(prefix) + branch + str(node.value) + ' (leaf)')

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a new value to the tree. duplicate values are allowed and get added
        to the right subtree of the already existing node with that value.
        """

        new_node = BSTNode(value)

        if self._root is None:
            self._root = new_node
            return

        current = self._root
        while current is not None:
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right



    def remove(self, value: object) -> bool:
        """
        Removes a value from the tree. Return True if the value was found,
        False otherwise.
        """
        parent = None
        current = self._root

        while current is not None:
            if value == current.value:
                if current.left is None and current.right is None:
                    self._remove_no_subtrees(parent, current)

                elif current.left is None or current.right is None:
                        self._remove_one_subtree(parent, current)

                else:
                        self._remove_two_subtrees(parent, current)

                return True

            elif value < current.value:
                parent = current
                current = current.left
            else:
                parent = current
                current = current.right

        return False





    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        removes a node that has no children (leaf node).
        Just need to update the parent's pointer to None
        """
        # remove node that has no subtrees (no left or right nodes)
        if remove_parent is None:
            self._root = None

        elif remove_parent.left == remove_node:
            remove_parent.left = None

        else:
            remove_parent.right = None


    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        removes a node that has one child.
        Child moves up to take the removed node's place.
        """
        if remove_node.left is not None:
            child = remove_node.left

        else:
            child = remove_node.right

        if remove_parent is None:
            self._root = child

        elif remove_parent.left == remove_node:
            remove_parent.left = child

        else:
            remove_parent.right = child

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        removes a node that has two children.
        finds the leftmost node in right subtree, copies its value
        to the node being removed and deletes the successor.
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



    def contains(self, value: object) -> bool:
        """
        returns True if the tree contains a given value, False otherwise.

        """
        current = self._root
        while current is not None:
            if value == current.value:
                return True

            elif value < current.value:
                current = current.left

            else:
                current = current.right

        return False



    def inorder_traversal(self) -> Queue:
        """
        performs an inorder traversal of the tree and returns a Queue containing
        sorted values from smallest to largest.
        """

        result = Queue()

        self._inorder_helper(self._root, result)

        return result


    def _inorder_helper(self, node: BSTNode, result: Queue) -> None:
        """
        recursive helper method for inorder traversal
        visits nodes in order from left subtree, current node, right subtree.
        """
        if node is None:
            return

        self._inorder_helper(node.left, result)

        result.enqueue(node.value)

        self._inorder_helper(node.right, result)



    def find_min(self) -> object:
        """
        finds the smallest value in the tree
        """
        if self._root is None:
            return None

        current = self._root

        while current.left is not None:
            current = current.left

        return current.value




    def find_max(self) -> object:
        """
        finds the maximum value in the tree
        """
        if self._root is None:
            return None

        current = self._root

        while current.right is not None:
            current = current.right

        return current.value

    def is_empty(self) -> bool:
        """
        returns True if the tree is empty, False otherwise.
        """
        if self._root is None:
            return True
        else:
            return False

    def make_empty(self) -> None:
        """
        removes all nodes from the tree

        """

        self._root = None


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, 'DEL:', del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, 'DEL:', del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
