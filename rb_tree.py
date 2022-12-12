import sys
import graphviz
import os

BLACK = 'black'
RED = 'red'

class Node:
    def __init__(self, key, color, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.color = color
        self.parent = parent

    def __str__(self):
        left = self.left.key if self.left else None
        right = self.right.key if self.right else None
        parent = self.parent.key if self.parent else None
        return 'key: {}, left: {}, right: {}, color: {}, parent: {}'.format(self.key, left, right, self.color, parent)


class RBTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = Node(key, BLACK)
        else:
            current = self.root
            while current:
                if key < current.key:
                    if not current.left:
                        new_node = Node(key, RED, current)
                        current.left = new_node
                        break
                    current = current.left
                else:
                    if not current.right:
                        new_node = Node(key, RED, current)
                        current.right = new_node
                        break
                    current = current.right
            self.fix_tree(new_node)

    def fix_tree(self, node):
        while node.parent and node.parent.color == RED:
            grand_parent = node.parent.parent #дедушка узла
            if node.parent == grand_parent.left:
                uncle = grand_parent.right

                if not uncle or uncle.color == BLACK:  # дядя отсутствует или черный
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = BLACK
                    grand_parent.color = RED
                    self.right_rotate(grand_parent)
                else: # иначе дядя красный
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    grand_parent.color = RED
                    node = grand_parent
            else: #если родитель нового узла правый сын
                uncle = grand_parent.left

                if not uncle or uncle.color == BLACK:  # дядя отсутствует или черный
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = BLACK
                    grand_parent.color = RED
                    self.left_rotate(grand_parent)
                else:  # иначе дядя красный
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    grand_parent.color = RED
                    node = grand_parent
        if self.root.color == RED:
            self.root.color = BLACK

    def left_rotate(self, node): # node - отец нового элемента
        if not node.right:
            return
        new_node = node.right
        node.right = new_node.left #LB

        if new_node.left:
            new_node.left.parent = node
        new_node.parent = node.parent
        if not node.parent:
            self.root = new_node
        else:
            if node == node.parent.left:
                node.parent.left = new_node
            else:
                node.parent.right = new_node
        new_node.left = node
        node.parent = new_node

    def right_rotate(self, node):
        if not node.left:
            return
        new_node = node.left
        node.left = new_node.right  # RB

        if new_node.right:
            new_node.right.parent = node
        new_node.parent = node.parent
        if not node.parent:
            self.root = new_node
        else:
            if node == node.parent.left:
                node.parent.left = new_node
            else:
                node.parent.right = new_node
        new_node.right = node
        node.parent = new_node


def breadth_first_search_graphviz(root, dot):
    queue = [root]
    dot.node(str(root.key), color=root.color)
    while queue:
        tmp_queue = []
        for element in queue:
            if element.left:
                dot.node(str(element.left.key), color=element.left.color)
                dot.edge(str(element.key), str(element.left.key))
                tmp_queue.append(element.left)
            if element.right:
                dot.node(str(element.right.key), color=element.right.color)
                dot.edge(str(element.key), str(element.right.key))
                tmp_queue.append(element.right)
        queue = tmp_queue

def breadth_first_search(root):
    queue = [root]
    current_level = 1
    while queue:
        tmp_queue = []
        print("------------------{}------------------".format(current_level))
        current_level += 1
        for element in queue:
            print(element)
            if element.left:
                tmp_queue.append(element.left)
            if element.right:
                tmp_queue.append(element.right)
        queue = tmp_queue
        print()

def clear_all_directory():
    dir = 'result'
    for f in os.listdir(dir): #clear previous info
        os.remove(os.path.join(dir, f))

def clear_gv_files():
    dir = 'result'
    for f in os.listdir(dir):
        if '.pdf' not in f:
            os.remove(os.path.join(dir, f))


if __name__ == '__main__':
    clear_all_directory()
    nodes = list(map(int, input().split()))
    rb_tree = RBTree()
    for index, node in enumerate(nodes):
        dot = graphviz.Digraph()
        rb_tree.insert(node)
        breadth_first_search_graphviz(rb_tree.root, dot)
        dot.render('result/g{}.gv'.format(index))
    breadth_first_search(rb_tree.root)
    clear_gv_files()