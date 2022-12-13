import random

DELETED = 'deleted' # для обработки удалений элементов. P.S. довольно неэффективно

class Probe:
    def __init__(self, key = None, idx = None):
        self.key = key
        self.idx = idx

    def __str__(self):
        return 'key: {}, cell: {}'.format(self.key, self.idx)

    def __eq__(self, other):
        return self.key == other.key


class HashTable:
    def __init__(self, size):
        self.size = size
        self.current_size = 0
        self.table = [None for _ in range(self.size)]
        self.hash_type = 'linear'
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

    def hashing(self, key, idx):
        if self.hash_type == 'linear':
            return self.linear_hashing(key, idx)
        elif self.hash_type == 'quadratic':
            return self.quadratic_hashing(key, idx)

    def linear_hashing(self, key, idx):
        hash_value = abs(key) % self.size + idx % self.size
        return hash_value % self.size

    def quadratic_hashing(self, key, idx):
        hash_value = abs(key) % self.size + pow(idx, 2, self.size)
        return hash_value % self.size

    def insert(self, key):
        idx = 0
        while True:
            hash_value = self.hashing(key, idx)
            if not self.table[hash_value] or self.table[hash_value].key == DELETED: # если нет такого ключа
                self.table[hash_value] = Probe(key, hash_value)
                self.current_size += 1
                if self.current_size >= 0.75 * self.size:
                    self.resize()
                break
            else:
                idx += 1 #ищем дальше свободное место

    def delete(self, key):
        if self.current_size == 0:
            print('Хеш-таблица пустая. Элемент {} нельзя удалить'.format(key))
            return
        for idx in range(self.size):
            hash_value = self.hashing(key, idx)
            if  self.table[hash_value] and self.table[hash_value].key != DELETED and self.table[hash_value].key == key:  # если ключ найден
                self.table[hash_value].key = DELETED
                self.current_size -= 1
                return hash_value
        print('Элемент с ключом {} не удален, так как не найден в хеш-таблице'.format(key))
        return None

    def search(self, key):
        if self.current_size == 0:
            print('Хеш-таблица пустая. Элемент {} отсутствует'.format(key))
            return
        for idx in range(self.size):
            hash_value = self.hashing(key, idx)
            if self.table[hash_value] and self.table[hash_value].key != DELETED and self.table[hash_value].key == key:  # если ключ найден
                print('Элемент найден в хеш-таблице: {}'.format(self.table[hash_value]))
                return hash_value
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
    #for i in range(100):
    hash_table.delete(5)
    print(hash_table)
    hash_table.insert(5)
    print(hash_table)
