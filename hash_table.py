import random
import time
import itertools

DELETED = 'deleted' # для обработки удалений элементов

class Probe:
    def __init__(self, key = None, idx = None):
        self.key = key
        self.idx = idx

    def __str__(self):
        return 'key: {}, idx: {}'.format(self.key, self.idx)

    def __eq__(self, other):
        return self.key == other.key


class HashTable:
    def __init__(self, size):
        self.size = size
        self.current_size = 0
        self.table = [None for _ in range(self.size)]
        self.hash_type = 'linear'
        self.k = 3  # фиксированный интервал между ячейками при линейном пробировани
        #Для того, чтобы все ячейки оказались просмотренными по одному разу, необходимо,
        # чтобы k было взаимно-простым с размером хеш-таблицы.
        self.c1 = 0 # \
                    #  | коэффициенты при квадратичном пробировании
        self.c2 = 1 # /
        self.choose_hash_type()

    def choose_hash_type(self):
        print('Выберите функцию для последовательности проб: linear, quadratic')
        hash_type = input()
        if hash_type in ['linear', 'quadratic']:
            self.hash_type = hash_type
        else:
            print('По умолчанию выбрано линейное пробирование')
            self.hash_type = 'linear'

    def resize(self):
        self.table += [None for _ in range(self.size)]
        self.size *= 2

    def hashing(self, hash_value, i):
        if self.hash_type == 'linear':
            return self.linear_hashing(hash_value, i)
        elif self.hash_type == 'quadratic':
            return self.quadratic_hashing(hash_value, i)

    def linear_hashing(self, hash_value, i):
        cell_number = (hash_value + (i * self.k) % self.size) % self.size
        return cell_number

    def quadratic_hashing(self, hash_value, i):
        cell_number = ((hash_value + self.c1 * i) % self.size + self.c2 * pow(i, 2, self.size)) % self.size
        return cell_number

    def hash_function(self, key):
        return key % self.size

    def insert(self, key):
        idx = 0
        hash_value = self.hash_function(key)
        while True:
            cell_number = self.hashing(hash_value, idx)
            if not self.table[cell_number] or self.table[cell_number].key == DELETED: # если нет такого ключа или он был удален
                self.table[cell_number] = Probe(key, cell_number)
                self.current_size += 1
                if self.current_size >= 0.66 * self.size:
                    self.resize()
                break
            else:
                idx += 1 #ищем дальше свободное место

    def delete(self, key):
        if self.current_size == 0:
            print('Хеш-таблица пустая. Элемент {} нельзя удалить'.format(key))
            return
        hash_value = self.hash_function(key)
        for idx in range(self.size):
            cell_number = self.hashing(hash_value, idx)
            if  self.table[cell_number] and self.table[cell_number].key != DELETED and self.table[cell_number].key == key:  # если ключ найден
                self.table[cell_number].key = DELETED
                self.current_size -= 1
                return
        print('Элемент с ключом {} не удален, так как не найден в хеш-таблице'.format(key))

    def search(self, key):
        if self.current_size == 0:
            print('Хеш-таблица пустая. Элемент {} отсутствует'.format(key))
            return
        hash_value = self.hash_function(key)
        for idx in range(self.size):
            cell_number = self.hashing(hash_value, idx)
            if self.table[cell_number] and self.table[cell_number].key != DELETED and self.table[cell_number].key == key:  # если ключ найден
                #print('Элемент найден в хеш-таблице: {}'.format(self.table[hash_value]))
                return cell_number
        print('Элемент с ключом {} не найден в хеш-таблице'.format(key))
        return None

    def __str__(self):
        str_table = []
        for i in range(self.size):
            if self.table[i]:
                str_table.append(str(self.table[i]))
        return 'Hash table size: {} (current size: {}), hash table: {}'.format(self.size, self.current_size, str(str_table))


if __name__ == '__main__':
    hash_table = HashTable(1000)
    hash_table.insert(5)
    hash_table.insert(5)
    random_number = random.randint(0, 150)
    hash_table.search(random_number)
    # for i in range(100):
    hash_table.delete(5)
    print(hash_table)
    hash_table.insert(8)
    print(hash_table)