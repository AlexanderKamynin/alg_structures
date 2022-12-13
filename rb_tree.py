import sys
import graphviz
import os
import copy

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
        self.nil = Node(-1, BLACK)

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
            self.fix_insert(new_node)

    def fix_insert(self, node):
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

    def fix_delete(self, node):
        while node != self.root and node.color == BLACK:
            if node == node.parent.left:
                brother = node.parent.right
                if brother.color == RED:
                    brother.color = BLACK
                    node.parent.color = RED
                    self.left_rotate(node.parent)
                    brother = node.parent.right
                # Если оба ребенка черные
                if (brother.left == None or brother.left.color == BLACK) and (brother.right == None or brother.right.color == BLACK):
                    brother.color = RED
                    node = node.parent
                else:
                    if brother.right.color == BLACK:
                        brother.left.color = BLACK
                        brother.color = RED
                        self.right_rotate(brother)
                        brother = node.parent.right
                    brother.color = node.parent.color
                    node.parent.color = BLACK
                    brother.right.color = BLACK
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                brother = node.parent.left
                if brother.color == RED:
                    brother.color = BLACK
                    node.parent.color = RED
                    self.right_rotate(node.parent)
                    brother = node.parent.left
                # Если оба ребенка черные
                if (brother.left == None or brother.left.color == BLACK) and (brother.right == None or brother.right.color == BLACK):
                    brother.color = RED
                    node = node.parent
                else:
                    if brother.left.color == BLACK:
                        brother.right.color = BLACK
                        brother.color = RED
                        self.left_rotate(brother)
                        brother = node.parent.left
                    brother.color = node.parent.color
                    node.parent.color = BLACK
                    brother.left.color = BLACK
                    self.right_rotate(node.parent)
                    node = self.root
        node.color = BLACK

    def change_nodes(self, node1, node2):
        if not node1.parent:
            self.root = node2
        elif node1 == node1.parent.left:
            node1.parent.left = node2
        else:
            node1.parent.right = node2
        node2.parent = node1.parent

    def delete(self, key):
        node_to_delete = Node(key, BLACK)
        node = self.root
        while node:
            if node.key == key:
                node_to_delete = node
            if node.key <= key:
                node = node.right
            else:
                node = node.left
        if not node_to_delete:
            print("Node with {0} key doesn't exist".format(key))
            return

        if not node_to_delete.left:
            node_to_delete.left = self.nil
            self.nil.parent = node_to_delete
        if not node_to_delete.right:
            node_to_delete.right = self.nil
            self.nil.parent = node_to_delete

        if node_to_delete.left == self.nil or node_to_delete.right == self.nil:
            y = node_to_delete
        else:
            y = self.successor(node_to_delete)
            if not y.left:
                y.left = self.nil
                self.nil.parent = y
            if not y.right:
                y.right =  self.nil
                self.nil.parent = y

        if y.left != self.nil:
            x = y.left
        else:
            x = y.right
        x.parent = y.parent

        if y.parent == None:
            self.root = x
        elif y == y.parent.left:
                y.parent.left = x
        else:
                y.parent.right = x

        if y != node_to_delete:
            node_to_delete = copy.deepcopy(y)
        if y.color == BLACK:
            self.fix_delete(x)

        if y.parent.left == self.nil:
            y.parent.left = None
        if y.parent.right == self.nil:
            y.parent.right = None
        self.nil.parent = None
        return y

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

    def min_node(self, node):
        if node:
            while node.left:
                node = node.left
            return node
        else:
            return node

    def successor(self, node):
        if node.right != None:
            return self.min_node(node.right)
        y = node.parent
        while y != None and x == y.right:
            x = y
            y = y.parent
        return y

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
    print('Выберите узлы к добавлению в дерево')
    nodes = list(map(int, input().split()))
    rb_tree = RBTree()
    for index, node in enumerate(nodes):
        dot = graphviz.Digraph()
        rb_tree.insert(node)
        breadth_first_search_graphviz(rb_tree.root, dot)
        dot.render('result/g{}.gv'.format(index))
    breadth_first_search(rb_tree.root)

    print('Выберите узлы к удалению')
    nodes = list(map(int, input().split()))
    if len(nodes) != 0:
        for index, node in enumerate(nodes):
            dot = graphviz.Digraph()
            rb_tree.delete(node)
            breadth_first_search_graphviz(rb_tree.root, dot)
            dot.render('result/g{}.gv'.format(index))
        breadth_first_search(rb_tree.root)

    clear_gv_files()