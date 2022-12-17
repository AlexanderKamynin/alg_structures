import sys
import graphviz
import os
import random
import copy
import time

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
        self.count_not_delete_nodes = 0
        self.root = None
        self.nil = Node(-1, BLACK)

    def search(self, key): #итеративный поиск
        current = self.root
        if not current or current == self.nil:
            print('RB-дерево пустое')
            return
        while current and current.key != key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        if not current:
            print('Узла с ключом {} нет'.format(key))
            return
        print('Ключ найден: {}'.format(str(current)))
        return current

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
                    #если правый черный или None
                    if brother.right == None or brother.right.color == BLACK:
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
                    if brother.left == None or brother.left.color == BLACK:
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
        if not node2:
            node2 = self.nil
        node2.parent = node1.parent

    def delete(self, key):
        node_to_delete = Node(key, BLACK)
        node = self.root
        if node == self.nil:
            print("Node with {0} key doesn't exist. Tree is empty".format(key))
            self.count_not_delete_nodes += 1
            return
        while node:
            if node.key == key:
                node_to_delete = node
            if node.key <= key:
                node = node.right
            else:
                node = node.left
        if not node_to_delete:
            print("Node with {0} key doesn't exist".format(key))
            self.count_not_delete_nodes += 1
            return

        if not node_to_delete.left:
            node_to_delete.left = self.nil
            self.nil.parent = node_to_delete
        if not node_to_delete.right:
            node_to_delete.right = self.nil
            self.nil.parent = node_to_delete

        y = node_to_delete
        y_origin_color = y.color
        if node_to_delete.left == self.nil:
            # у элемента нет левого сына
            x = node_to_delete.right
            self.change_nodes(node_to_delete, node_to_delete.right)
        elif (node_to_delete.right == self.nil):
            # у элемента нет правого сына
            x = node_to_delete.left
            self.change_nodes(node_to_delete, node_to_delete.left)
        else:
            # есть оба ребенка
            y = self.min_node(node_to_delete.right)
            y_origin_color = y.color
            x = y.right
            if not x:
                x = self.nil
            if y.parent == node_to_delete: # если y - ребенок node_to_delete
                x.parent = y
            else:
                self.change_nodes(y, y.right)
                y.right = node_to_delete.right
                y.right.parent = y
            self.change_nodes(node_to_delete, y)
            y.left = node_to_delete.left
            y.left.parent = y
            y.color = node_to_delete.color
        if y_origin_color == BLACK:
            self.fix_delete(x)

        if y.parent and y.parent.left == self.nil:
            y.parent.left = None
        if y.parent and y.parent.right == self.nil:
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
            if not node:
                node = self.nil
            return node
        else:
            return self.nil

    def successor(self, node):
        if node.right != None:
            return self.min_node(node.right)
        y = node.parent
        while y != None and x == y.right:
            x = y
            y = y.parent
        return y
    def print(self, output_name):
        que = [self.root]
        dot = graphviz.Digraph()
        dot.attr('node', fontsize='20')
        def print_node(node, parent_id=''):
            node_id = str(id(node))
            shape = 'ellipse' if node.key is not None else 'rectangle'
            dot.node(node_id, label=str(node.key), color=node.color, fontcolor=node.color, shape=shape)
            if parent_id:
                dot.edge(parent_id, node_id)
        print_node(self.root)
        dot.format = 'png'
        while que:
            tmp_que = []
            for el in que:
                el_id = str(id(el))
                if el.left:
                    print_node(el.left, el_id)
                    tmp_que.append(el.left)
                if el.right:
                    print_node(el.right, el_id)
                    tmp_que.append(el.right)
            que = tmp_que
        dot.render('result/{}'.format(output_name))

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

def manual_input():
    clear_all_directory()
    print('Выберите узлы к добавлению в дерево')
    nodes = list(map(int, input().split()))
    rb_tree = RBTree()
    for index, node in enumerate(nodes):
        rb_tree.insert(node)
    rb_tree.print('insert')
    breadth_first_search(rb_tree.root)

def good_test(): # последовательные элементы
    start = time.time()
    rb_tree = RBTree()
    for i in range(30):
        rb_tree.insert(i)
    end = time.time() - start
    print("Adding elements to rbtree table: {}".format(end))
    rb_tree.print('insert')
    start = time.time()
    cnt = 0
    try:
        for i in range(30):
            rb_tree.delete(i)
            #rb_tree.print(str(i))
            cnt += 1
    except:
        print("Ошибка блин")
    end = time.time() - start
    # breadth_first_search(rb_tree.root)
    print("Удалось удалить {} элементов".format(cnt))
    print("Элементов не было удалено {}".format(rb_tree.count_not_delete_nodes))
    print("Removing elements from tree table: {}".format(end))

def not_good_test(): # перемешанные элементы с помощью функции shuffle() модуля random
    nodes_to_add = []
    for i in range(14000000):
        nodes_to_add.append(i)
    random.shuffle(nodes_to_add)
    rb_tree = RBTree()
    start = time.time()
    for i in range(14000000):
        rb_tree.insert(nodes_to_add[i])
    end = time.time() - start
    print("Adding elements to rbtree table: {}".format(end))
    #breadth_first_search(rb_tree.root)
    start = time.time()
    cnt = 0
    try:
        for i in range(14000000):
            rb_tree.delete(i)
            cnt += 1
    except:
        print("Ошибка блин")
    end = time.time() - start
    #breadth_first_search(rb_tree.root)
    print("Удалось удалить {} элементов".format(cnt))
    print("Элементов не было удалено {}".format(rb_tree.count_not_delete_nodes))
    print("Removing elements from tree table: {}".format(end))

def check_search_time(): # поиск случайного числа в диапозоне 0-100000 в RB-дереве
    nodes_to_add = []
    for i in range(1000000):
        nodes_to_add.append(i)
    random.shuffle(nodes_to_add)
    rb_tree = RBTree()
    for i in range(1000000):
        rb_tree.insert(nodes_to_add[i])
    random_number = random.randint(0, 100000)
    start = time.time()
    rb_tree.search(random_number)
    end = time.time() - start
    print("Поиск элемента в RB-дереве: {}".format(end))

def manual_checks():
    clear_all_directory()
    nodes = []
    for i in range(2222):
        nodes.append(str(i))
    rb_tree = RBTree()
    for index, node in enumerate(nodes):
        rb_tree.insert(node)
    rb_tree.print('insert')
    # breadth_first_search(rb_tree.root)

if __name__ == '__main__':
    clear_all_directory()
    # good_test()
    not_good_test()
    # check_search_time()
    # manual_input()
    # manual_checks()
