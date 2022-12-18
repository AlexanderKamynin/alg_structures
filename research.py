import time
import sys
import graphviz
import os
import copy
import hash_table
import rb_tree
import random
import matplotlib.pyplot as plt
import numpy


def clear_all_directory():
    dir = 'result'
    for f in os.listdir(dir): #clear previous info
        os.remove(os.path.join(dir, f))

def rb_tree_manual_input(): #пользовательская проверка работы дерева и корректности реализации rb-tree
    clear_all_directory()
    print('Введите ключи к добавлению в дерево')
    nodes = list(map(int, input().split()))
    rb_tree = RBTree()
    for index, node in enumerate(nodes):
        rb_tree.insert(node)
    rb_tree.print('insert')
    breadth_first_search(rb_tree.root)

def create_graphics(n, times, title_name): #создать график на основе кол-ва элементов и массива times
    plt.figure()
    plt.title(title_name)
    plt.plot(n, times, color='#065780')
    plt.xlabel("n, кол-во элементов")
    plt.ylabel("t, сек")
    plt.savefig("result/{}.png".format(title_name))

def average_case_rb_tree_insert():
    print('Average-insert case for RB-tree processing...')
    nodes_to_add = []
    count = 1000000
    n = [i for i in range(1, count)]
    nodes_to_add = [i for i in range(1, count)]
    random.shuffle(nodes_to_add)
    times = []
    tree = rb_tree.RBTree()
    start = time.perf_counter()
    for elem in nodes_to_add:
        tree.insert(elem)
        times.append(time.perf_counter() - start)
    create_graphics(n, times, "RB-tree, average-case for insert")

def average_case_rb_tree_delete():
    print('Delete case for RB-tree processing...')
    nodes_to_add = []
    tree = rb_tree.RBTree()
    count = 1000000
    n = [i for i in range(1, count)]
    nodes_to_add = [i for i in range(1, count)]
    random.shuffle(nodes_to_add)
    for elem in nodes_to_add:
        tree.insert(elem)
    random.shuffle(nodes_to_add)
    times = []
    start = time.perf_counter()
    for elem in nodes_to_add:
        tree.delete(elem)
        times.append(time.perf_counter() - start)
    create_graphics(n, times, "RB-tree, average-case for delete")
    tree.print('tree_deleting')

def average_case_rb_tree_search():
    print('Search case for RB-tree processing...')
    nodes_to_add = []
    tree = rb_tree.RBTree()
    count = 1000000
    n = [i for i in range(1, count)]
    nodes_to_add = [i for i in range(1, count)]
    random.shuffle(nodes_to_add)
    for elem in nodes_to_add:
        tree.insert(elem)
    random.shuffle(nodes_to_add)
    times = []
    start = time.perf_counter()
    for elem in nodes_to_add:
        tree.search(elem)
        times.append(time.perf_counter() - start)
    create_graphics(n, times, "RB-tree, average-case for search")

def good_case_rb_tree_insert(): # добавляемые ключи соответсвуют обходу в ширину
    print('Good case for RB-tree processing...')
    count = 1000000
    n = [i for i in range(1, count)]
    tree = rb_tree.RBTree()
    for elem in range(1, count):
        tree.insert(elem)
    nodes_to_add = rb_tree.breadth_first_search(tree.root)
    del tree
    tree = rb_tree.RBTree()
    times = []
    start = time.perf_counter()
    for elem in nodes_to_add:
        tree.insert(elem)
        times.append(time.perf_counter() - start)
    create_graphics(n, times,  "RB-tree, good-case for insert")


if __name__ == '__main__':
    clear_all_directory()
    average_case_rb_tree_insert()
    average_case_rb_tree_delete()
    average_case_rb_tree_search()
    print('Research is complete! Check */result folder')