import time
import sys
import graphviz
import os
import gc
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
    print('Enter the count of pair (key,value) for add in rb-tree')
    count = int(input())
    print('Enter the pairs (key,value) to add in rb-tree')
    nodes_to_add = []
    for i in range(count):
        node = list(map(int, input().split()))
        nodes_to_add.append(node)
    tree = rb_tree.RBTree()
    for node in nodes_to_add:
        tree.insert(node[0], node[1])
    tree.print('rb_tree_graphviz')
    print('Enter the key to delete')
    keys_to_delete = list(map(int, input().split()))
    for keys in keys_to_delete:
        tree.delete(keys)
    tree.print('rb_tree_after_delete')

def hash_table_manual_input(): #пользовательская проверка работы хеш-таблицы и корректности ее реализации
    print('Enter the count of pair (key,value) for add in hash-table')
    count = int(input())
    print('Enter the pairs (key,value) to add in hash-table')
    nodes_to_add = []
    for i in range(count):
        node = list(map(int, input().split()))
        nodes_to_add.append(node)
    table = hash_table.HashTable(100)
    for node in nodes_to_add:
        table.insert(node[0], node[1])
    print(table)
    print('Enter the key to delete')
    keys_to_delete = list(map(int, input().split()))
    for keys in keys_to_delete:
        table.delete(keys)
    print('Table after delete')
    print(table)

def create_graphics_with_log(n, times, title_name): #создать график на основе кол-ва элементов и массива times
    plt.figure()
    plt.title(title_name)
    plt.xlabel("n, count")
    plt.ylabel("t, ns")
    plt.scatter(n, times, s=0.5, color='blue')
    plt.plot(n, numpy.log2(n) * 10**3, color='green')
    plt.savefig("result/{}.png".format(title_name))
    plt.show()

def create_graphics(n, times, title_name):
    plt.figure()
    plt.title(title_name)
    plt.xlabel("n, count")
    plt.ylabel("t, ns")
    plt.scatter(n, times, s=0.2, color='orange')
    plt.savefig("result/{}.png".format(title_name))
    plt.show()

def create_compared_graphics(n, times_tree, times_table, title_name):
    plt.figure()
    plt.title(title_name)
    plt.xlabel("n, count")
    plt.ylabel("t, ns")
    plt.scatter(n, times_tree, s=0.2, color='blue', label='rb-tree')
    plt.scatter(n, times_table, s=0.2, color='orange', label='hash-table')
    plt.legend(loc="best")
    plt.savefig("result/{}.png".format(title_name))
    plt.show()


def average_case_rb_tree_insert():
    print('Average-case for RB-tree inserting...')
    count = 10001
    research_count = 100
    n = [i for i in range(1, count)]
    insert_time = [0 for _ in range(1, count)]
    for i in range(research_count):
        nodes_to_add = [[random.randint(0, int(2*count)), random.randint(0, 1000)] for i in range(1, count)]
        random.shuffle(nodes_to_add)
        tree = rb_tree.RBTree()
        for idx, elem in enumerate(nodes_to_add):
            gc.disable() #отключение сборщика мусора
            start = time.perf_counter_ns()
            tree.insert(elem[0], elem[1])
            end = time.perf_counter_ns() - start
            gc.enable()
            insert_time[idx] += end
        del tree
    for i in range(len(insert_time)):
        insert_time[i] /= research_count
    create_graphics_with_log(n, insert_time, "RB-tree, average-case for insert")

def average_case_rb_tree_delete():
    print('Average-case for RB-tree deleting...')
    count = 10001
    research_count = 100
    n = [i for i in range(1, count)]
    delete_time = [0 for i in range(1, count)]
    for i in range(research_count):
        nodes_to_add = [[random(count*3, count*5), random.randint(0, 1000)] for i in range(1, count)]
        random.shuffle(nodes_to_add)
        tree = rb_tree.RBTree()
        for elem in nodes_to_add:
            tree.insert(elem[0], elem[1])
        for j in range(1, count):
            idx = random.randint(0, len(nodes_to_add) - 1)
            key_to_delete = nodes_to_add[idx][0]
            gc.disable()
            start = time.perf_counter_ns()
            tree.delete(key_to_delete)
            end = time.perf_counter_ns() - start
            gc.enable()
            delete_time[j-1] += end
            nodes_to_add.pop(idx)
        del tree
    delete_time.reverse()
    for i in range(len(delete_time)):
        delete_time[i] /= research_count
    create_graphics_with_log(n, delete_time, "RB-tree, average-case for delete")

def average_case_rb_tree_search():
    print('Average-case for RB-tree searching...')
    count = 10001
    research_count = 100
    n = [i for i in range(1, count)]
    search_time = [0 for i in range(1, count)]
    for i in range(research_count):
        nodes_to_add = [[i, random.randint(0, 1000)] for i in range(1, count)]
        random.shuffle(nodes_to_add)
        tree = rb_tree.RBTree()
        for elem in nodes_to_add:
            tree.insert(elem[0], elem[1])
        for j in range(1, count):
            idx = random.randint(0, len(nodes_to_add) - 1)
            key_to_search = nodes_to_add[idx][0]
            gc.disable()
            start = time.perf_counter_ns()
            tree.search(key_to_search)
            end = time.perf_counter_ns() - start
            gc.enable()
            search_time[j-1] += end
            tree.delete(key_to_search)
            nodes_to_add.pop(idx)
    search_time.reverse()
    for i in range(len(search_time)):
        search_time[i] /= research_count
    create_graphics_with_log(n, search_time, "RB-tree, average-case for search")

def average_case_hash_table_insert(hash_type):
    print('Hash-table inserting...')
    count = 10001
    research_count = 100
    n = [i for i in range(1, count)]
    insert_time = [0 for _ in range(1, count)]
    for i in range(research_count):
        nodes_to_add = [[random.randint(0, count), random.randint(0, 1000)] for i in range(1, count)]
        times = []
        table = hash_table.HashTable(count * 3, hash_type)
        for idx, node in enumerate(nodes_to_add):
            gc.disable() #отключение сборщика мусора
            start = time.perf_counter_ns()
            table.insert(node[0], node[1])
            end = time.perf_counter_ns() - start
            gc.enable()
            insert_time[idx] += end
        del table
    for i in range(len(insert_time)):
        insert_time[i] /= research_count
    create_graphics(n, insert_time, "Hash-table, average insert, {}".format(hash_type))

def average_case_hash_table_delete(hash_type):
    print('Average-case for Hash-table deleting...')
    count = 10001
    research_count = 100
    n = [i for i in range(1, count)]
    delete_time = [0 for i in range(1, count)]
    for i in range(research_count):
        nodes_to_add = [[random.randint(0, count*2), random.randint(0, 1000)] for i in range(1, count)]
        table = hash_table.HashTable(count * 3, hash_type)
        for node in nodes_to_add:
            table.insert(node[0], node[1])
        for j in range(1, count):
            idx = random.randint(0, len(nodes_to_add) - 1)
            key_to_delete = nodes_to_add[idx][0]
            gc.disable()
            start = time.perf_counter_ns()
            table.delete(key_to_delete)
            end = time.perf_counter_ns() - start
            gc.enable()
            delete_time[j - 1] += end
            nodes_to_add.pop(idx)
        del table
    delete_time.reverse()
    for i in range(len(delete_time)):
        delete_time[i] /= research_count
    create_graphics(n, delete_time, "Hash-table, average-case for delete, {}".format(hash_type))

def average_case_hash_table_search(hash_type):
    print('Average-case for Hash-table searching...')
    count = 10001
    research_count = 1
    n = [i for i in range(1, count)]
    search_time = [0 for i in range(1, count)]
    for i in range(research_count):
        nodes_to_add = [[random.randint(0, count*2), random.randint(0, 1000)] for i in range(1, count)]
        table = hash_table.HashTable(count * 3, hash_type)
        for node in nodes_to_add:
            table.insert(node[0], node[1])
        for j in range(1, count):
            idx = random.randint(0, len(nodes_to_add) - 1)
            key_to_search = nodes_to_add[idx][0]
            gc.disable()
            start = time.perf_counter_ns()
            table.search(key_to_search)
            end = time.perf_counter_ns() - start
            gc.enable()
            search_time[j - 1] += end
            table.delete(key_to_search)
            nodes_to_add.pop(idx)
        del table
    search_time.reverse()
    for i in range(len(search_time)):
        search_time[i] /= research_count
    create_graphics(n, search_time, "Hash-table, average-case for search, {}".format(hash_type))

def compare_insert(hash_type):
    print('RB-tree Vs Hash-table inserting...')
    count = 10001
    research_count = 100
    n = [i for i in range(1, count)]
    insert_time_tree = [0 for _ in range(1, count)]
    insert_time_table = [0 for _ in range(1, count)]
    for i in range(research_count):
        nodes_to_add = [[q, random.randint(0, 1000)] for q in range(1, count)]
        random.shuffle(nodes_to_add)
        tree = rb_tree.RBTree()
        table = hash_table.HashTable(count * 2, hash_type)
        for idx, elem in enumerate(nodes_to_add):
            gc.disable()  # отключение сборщика мусора
            start = time.perf_counter_ns()
            tree.insert(elem[0], elem[1])
            end = time.perf_counter_ns() - start
            gc.enable()
            insert_time_tree[idx] += end

            gc.disable()  # отключение сборщика мусора
            start = time.perf_counter_ns()
            table.insert(elem[0], elem[1])
            end = time.perf_counter_ns() - start
            gc.enable()
            insert_time_table[idx] += end
        del tree
        del table
    for i in range(len(n)):
        insert_time_tree[i] /= research_count
        insert_time_table[i] /= research_count
    create_compared_graphics(n, insert_time_tree, insert_time_table, "RB-tree Vs Hash-table ({}) insert".format(hash_type))

def compare_delete(hash_type):
    print('RB-tree Vs Hash-table deleting...')
    count = 10001
    research_count = 100
    n = [i for i in range(1, count)]
    delete_time_tree = [0 for i in range(1, count)]
    delete_time_table = [0 for i in range(1, count)]
    for i in range(research_count):
        nodes_to_add = [[q, random.randint(0, 1000)] for q in range(1, count)]
        random.shuffle(nodes_to_add)
        tree = rb_tree.RBTree()
        table = hash_table.HashTable(count * 2, hash_type)
        for elem in nodes_to_add:
            tree.insert(elem[0], elem[1])
            table.insert(elem[0], elem[1])
        for j in range(1, count):
            idx = random.randint(0, len(nodes_to_add) - 1)
            key_to_delete = nodes_to_add[idx][0]
            gc.disable()
            start = time.perf_counter_ns()
            tree.delete(key_to_delete)
            end = time.perf_counter_ns() - start
            gc.enable()
            delete_time_tree[j - 1] += end

            gc.disable()
            start = time.perf_counter_ns()
            table.delete(key_to_delete)
            end = time.perf_counter_ns() - start
            gc.enable()
            delete_time_table[j - 1] += end

            nodes_to_add.pop(idx)
        del tree
        del table
    delete_time_tree.reverse()
    delete_time_table.reverse()
    for i in range(len(n)):
        delete_time_tree[i] /= research_count
        delete_time_table[i] /= research_count
    create_compared_graphics(n, delete_time_tree, delete_time_table, "RB-tree Vs Hash-table ({}) delete".format(hash_type))

def compare_search(hash_type):
    print('RB-tree Vs Hash-table searching...')
    count = 10001
    research_count = 100
    n = [i for i in range(1, count)]
    search_time_tree = [0 for i in range(1, count)]
    search_time_table = [0 for i in range(1, count)]
    for i in range(research_count):
        nodes_to_add = [[q, random.randint(0, 1000)] for q in range(1, count)]
        random.shuffle(nodes_to_add)
        tree = rb_tree.RBTree()
        table = hash_table.HashTable(count * 2, hash_type)
        for elem in nodes_to_add:
            tree.insert(elem[0], elem[1])
            table.insert(elem[0], elem[1])
        for j in range(1, count):
            idx = random.randint(0, len(nodes_to_add) - 1)
            key_to_search = nodes_to_add[idx][0]
            gc.disable()
            start = time.perf_counter_ns()
            tree.search(key_to_search)
            end = time.perf_counter_ns() - start
            gc.enable()
            search_time_tree[j - 1] += end

            gc.disable()
            start = time.perf_counter_ns()
            table.search(key_to_search)
            end = time.perf_counter_ns() - start
            gc.enable()
            search_time_table[j - 1] += end

            table.delete(key_to_search)
            tree.delete(key_to_search)
            nodes_to_add.pop(idx)
        del tree
        del table
    search_time_tree.reverse()
    search_time_table.reverse()
    for i in range(len(n)):
        search_time_tree[i] /= research_count
        search_time_table[i] /= research_count
    create_compared_graphics(n, search_time_tree, search_time_table, "RB-tree Vs Hash-table ({}) search".format(hash_type))

def check_rb_tree():
    average_case_rb_tree_insert()
    average_case_rb_tree_delete()
    average_case_rb_tree_search()

def check_hash_table():
    print('Choose hash-type: linear, quadratic, double')
    hash_type = input()
    average_case_hash_table_insert(hash_type)
    average_case_hash_table_delete(hash_type)
    average_case_hash_table_search(hash_type)

def compare_structure():
    print('Choose hash-type: linear, quadratic, double')
    hash_type = input()
    compare_insert(hash_type)
    compare_delete(hash_type)
    compare_search(hash_type)

if __name__ == '__main__':
    clear_all_directory()
    rb_tree_manual_input()
    hash_table_manual_input()
    check_rb_tree()
    check_hash_table()
    compare_structure()
    print('Research is complete! Check */result folder')