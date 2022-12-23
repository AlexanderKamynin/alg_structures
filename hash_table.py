import random
import time

DELETED = 'deleted' # для обработки удалений элементов

class Node:
    def __init__(self, key = None, value = None):
        self.key = key
        self.value = value

    def __str__(self):
        return 'key: {}, value: {}'.format(self.key, self.value)

    def __eq__(self, other):
        if other == DELETED:
            return False
        return self.key == other.key


class HashTable:
    def __init__(self, size, hash_type=None):
        self.size = size
        self.current_size = 0
        self.table = [None for _ in range(self.size)]
        self.hash_type = hash_type
        self.k = 3  # фиксированный интервал между ячейками при линейном пробировани
        #Для того, чтобы все ячейки оказались просмотренными по одному разу, необходимо,
        # чтобы k было взаимно-простым с размером хеш-таблицы.
        self.c1 = 0 # \
                    #  | коэффициенты при квадратичном пробировании
        self.c2 = 1 # /
        self.choose_hash_type()

    def choose_hash_type(self):
        if not self.hash_type:
            print('Выберите функцию для последовательности проб: linear, quadratic, double')
            hash_type = input()
            if hash_type in ['linear', 'quadratic', 'double']:
                self.hash_type = hash_type
            else:
                print('По умолчанию выбрано линейное пробирование')
                self.hash_type = 'linear'
        else:
            return

    def resize(self):
        self.table += [None for _ in range(self.size)]
        self.size *= 2

    def hashing(self, i, hash_value=None, hash_value_first=None, hash_value_second=None):
        if self.hash_type == 'linear':
            return self.linear_hashing(hash_value, i)
        elif self.hash_type == 'quadratic':
            return self.quadratic_hashing(hash_value, i)
        elif self.hash_type == 'double':
            return self.double_hashing(hash_value_first, hash_value_second, i)

    def linear_hashing(self, hash_value, i):
        cell_number = (hash_value + (i * self.k) % self.size) % self.size
        return cell_number

    def quadratic_hashing(self, hash_value, i):
        cell_number = ((hash_value + self.c1 * i) % self.size + self.c2 * pow(i, 2, self.size)) % self.size
        return cell_number

    def double_hashing(self, hash_value_first, hash_value_second, i):
        cell_number = (hash_value_first + (i * hash_value_second) % self.size ) % self.size
        return cell_number

    def hash_function(self, key):
        return key % self.size

    def second_hash_function(self, key):
        return (key * 7 + 1) % self.size

    def insert(self, key, value):
        idx = 0
        if self.hash_type != 'double':
            hash_value = self.hash_function(key)
        else:
            first_hash_value = self.hash_function(key)
            second_hash_value = self.second_hash_function(key)
        while True:
            if self.hash_type != 'double':
                cell_number = self.hashing(idx, hash_value=hash_value)
            else:
                cell_number = self.hashing(idx, hash_value_first=first_hash_value, hash_value_second=second_hash_value)
            if not self.table[cell_number] or self.table[cell_number] == DELETED: # если нет такого ключа или он был удален
                self.table[cell_number] = Node(key, value)
                self.current_size += 1
                if self.current_size >= 0.88 * self.size:
                    self.resize()
                break
            else:
                if self.table[cell_number].key == key:
                    self.table[cell_number].value = value
                    break
                idx += 1 #ищем дальше свободное место

    def delete(self, key):
        if self.current_size == 0:
            #print('Хеш-таблица пустая. Элемент {} нельзя удалить'.format(key))
            return
        if self.hash_type != 'double':
            hash_value = self.hash_function(key)
        else:
            first_hash_value = self.hash_function(key)
            second_hash_value = self.second_hash_function(key)
        for idx in range(self.size):
            if self.hash_type != 'double':
                cell_number = self.hashing(idx, hash_value=hash_value)
            else:
                cell_number = self.hashing(idx, hash_value_first=first_hash_value, hash_value_second=second_hash_value)
            if  self.table[cell_number] and self.table[cell_number] != DELETED and self.table[cell_number].key == key:  # если ключ найден
                self.table[cell_number] = DELETED
                self.current_size -= 1
                return
        #print('Элемент с ключом {} не удален, так как не найден в хеш-таблице'.format(key))

    def search(self, key):
        if self.current_size == 0:
            #print('Хеш-таблица пустая. Элемент {} отсутствует'.format(key))
            return
        if self.hash_type != 'double':
            hash_value = self.hash_function(key)
        else:
            first_hash_value = self.hash_function(key)
            second_hash_value = self.second_hash_function(key)
        for idx in range(self.size):
            if self.hash_type != 'double':
                cell_number = self.hashing(idx, hash_value=hash_value)
            else:
                cell_number = self.hashing(idx, hash_value_first=first_hash_value, hash_value_second=second_hash_value)
            if self.table[cell_number] and self.table[cell_number] != DELETED and self.table[cell_number].key == key:  # если ключ найден
                #print('Элемент найден в хеш-таблице: {}'.format(self.table[hash_value]))
                return self.table[cell_number]
        #print('Элемент с ключом {} не найден в хеш-таблице'.format(key))
        return None

    def __str__(self):
        str_table = []
        for i in range(self.size):
            if self.table[i]:
                node_info = [str(self.table[i]), 'cell: {}'.format(i)]
                str_table.append(node_info)
        return 'Hash table size: {} (current size: {}), hash table: {}'.format(self.size, self.current_size, str(str_table))

