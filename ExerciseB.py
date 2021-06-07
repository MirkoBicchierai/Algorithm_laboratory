import random
import matplotlib.pyplot as plt


def doGraph(name, x_variable, y_variable):
    plt.plot(x_variable, y_variable)
    plt.savefig(name + '.png')
    plt.close()


def hash_func_linear(k, i, m):
    return (hash_func(k, m) + i) % m


def hash_func(k, m):
    return k % m


class HashTableCon:
    def __init__(self, n):
        self.collision = 0
        self.table = [[] for _ in range(n)]

    def print(self):
        print(self.table)

    def hash_insert(self, k):
        m = len(self.table)
        j = hash_func(k, m)
        if len(self.table[j]) != 0:
            self.collision += 1
        self.table[j].insert(0, k)

    def hash_delete(self, k):
        m = len(self.table)
        j = hash_func(k, m)
        if k in self.table[j]:
            self.table[j].remove(k)
        else:
            print("data don't exist")

    def hash_search(self, k):
        m = len(self.table)
        j = hash_func(k, m)
        if k in self.table[j]:
            print("data exist")
        else:
            print("data don't exist")


class HashTable:

    def __init__(self, n):
        self.collision = 0
        self.table = [None for _ in range(n)]

    def print(self):
        print(self.table)

    def hash_insert(self, k):
        i = 0
        while True:
            j = hash_func_linear(k, i, len(self.table))
            if self.table[j] is None or self.table[j] == "DELETED":
                self.table[j] = k
                return j
            else:
                i += 1
                self.collision += 1
            if i == len(self.table):
                break
        # print("hash table overflow")

    def hash_delete(self, k):
        i = 0
        while True:
            j = hash_func_linear(k, i, len(self.table))
            if self.table[j] == k:
                self.table[j] = "DELETED"
                return j
            else:
                i += 1
            if i == len(self.table) or self.table[j] is None:
                break
        print("key don't exist")
        return

    def hash_search(self, k):
        i = 0
        while True:
            j = hash_func_linear(k, i, len(self.table))
            if self.table[j] == k:
                return j
            else:
                i += 1
            if i == len(self.table) or self.table[j] is None:
                break
        print("key don't exist")
        return None


def test_insert(dim_table, dim_insert):
    insert_vector = [random.randint(1, 100) for _ in range(dim_insert)]

    table = HashTable(dim_table)
    for i in range(len(insert_vector)):
        table.hash_insert(insert_vector[i])
    table.print()

    table_con = HashTableCon(dim_table)
    for i in range(len(insert_vector)):
        table_con.hash_insert(insert_vector[i])
    table_con.print()

    print("Collision - chaining : " + str(table_con.collision))
    print("Collision - open addressing : " + str(table.collision))
    print("a: " + str(len(insert_vector) / len(table_con.table)))


def graph():
    insert_vector = [random.randint(1, 1000) for _ in range(1000)]

    table = HashTable(1000)
    for i in range(len(insert_vector)):
        table.hash_insert(insert_vector[i])

    table_con = HashTableCon(1000)
    for i in range(len(insert_vector)):
        table_con.hash_insert(insert_vector[i])

    vec_col_ind = [table.collision]
    vec_col_con = [table_con.collision]

    insert_vector = [random.randint(1, 1000) for _ in range(800)]
    table = HashTable(1000)
    for i in range(len(insert_vector)):
        table.hash_insert(insert_vector[i])

    table_con = HashTableCon(1000)
    for i in range(len(insert_vector)):
        table_con.hash_insert(insert_vector[i])

    vec_col_ind.append(table.collision)
    vec_col_con.append(table_con.collision)

    insert_vector = [random.randint(1, 1000) for _ in range(500)]
    table = HashTable(1000)
    for i in range(len(insert_vector)):
        table.hash_insert(insert_vector[i])

    table_con = HashTableCon(1000)
    for i in range(len(insert_vector)):
        table_con.hash_insert(insert_vector[i])

    vec_col_ind.append(table.collision)
    vec_col_con.append(table_con.collision)

    vec_col_ind = []
    vec_col_con = []

    for j in range(1000):

        insert_vector = [random.randint(1, 100000) for _ in range((j+1)*100)]
        table = HashTable(100000)
        for i in range(len(insert_vector)):
            table.hash_insert(insert_vector[i])

        table_con = HashTableCon(100000)
        for i in range(len(insert_vector)):
            table_con.hash_insert(insert_vector[i])

        vec_col_ind.append(table.collision)
        vec_col_con.append(table_con.collision)

    print(vec_col_con[[0.001*(j+1)for j in range(1000)].index(0.2)])
    print(vec_col_con[[0.001 * (j + 1) for j in range(1000)].index(0.4)])
    print(vec_col_con[[0.001*(j+1)for j in range(1000)].index(0.6)])
    print(vec_col_con[[0.001 * (j + 1) for j in range(1000)].index(0.8)])
    print(vec_col_con[[0.001*(j+1)for j in range(1000)].index(1)])

    print(vec_col_ind[[0.001*(j+1)for j in range(1000)].index(0.2)])
    print(vec_col_ind[[0.001 * (j + 1) for j in range(1000)].index(0.4)])
    print(vec_col_ind[[0.001*(j+1)for j in range(1000)].index(0.6)])
    print(vec_col_ind[[0.001 * (j + 1) for j in range(1000)].index(0.8)])
    print(vec_col_ind[[0.001*(j+1)for j in range(1000)].index(1)])

    doGraph("exerciseB_fold/collisioni_concatenamento", [0.001*(j+1)for j in range(1000)], vec_col_con)
    doGraph("exerciseB_fold/collisioni_indirizzamento_aperto", [0.001*(j+1)for j in range(1000)], vec_col_ind)


if __name__ == "__main__":
    test_insert(dim_insert=random.randint(1, 50), dim_table=10)
    graph()
