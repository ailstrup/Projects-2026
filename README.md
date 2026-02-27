BST (bst.py)
Binary Search Tree implementation in Python. Supports insertion (with duplicates), removal using inorder successor strategy, search, inorder traversal, and min/max operations. Handles all three removal cases: leaf nodes, single-child nodes, and two-child nodes.
AVL Tree (avl.py)
Self-balancing AVL Tree that extends the BST implementation. Maintains O(log n) operations through automatic rebalancing via left/right rotations after insertions and deletions. Tracks parent pointers and node heights, rejects duplicates, and includes balance factor calculation and validation methods.
