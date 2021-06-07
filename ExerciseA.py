import string
import random
from timeit import Timer
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import numpy as np


def getRandomWord(attempt, dictionary, dictionary_length):
    file = open(dictionary, 'r')
    n = random.randint(0, dictionary_length)
    query = ""
    for i in range(0, n):
        query = file.readline()
    while len(query) != attempt:
        query = file.readline()
    return query


def addCharacter(word):
    tmp = random.randint(0, len(word))
    return word[:tmp] + random.choice(string.ascii_letters) + word[tmp:]


def removeCharacter(word):
    tmp = random.randint(0, len(word))
    return word[:tmp] + word[(tmp + 1):]


def swapCharacter(word):
    while True:
        tmp = random.randint(0, len(word) - 1)
        tmp2 = random.randint(0, len(word) - 1)
        if tmp != tmp2:
            break

    if tmp < tmp2:
        if tmp2 == len(word) - 1:
            return word[:tmp] + word[tmp2] + word[tmp + 1:tmp2] + word[tmp]
        else:
            return word[:tmp] + word[tmp2] + word[tmp + 1:tmp2] + word[tmp] + word[tmp2 + 1:]
    elif tmp > tmp2:
        if tmp == len(word) - 1:
            return word[:tmp2] + word[tmp] + word[tmp2 + 1:tmp] + word[tmp2]
        else:
            return word[:tmp2] + word[tmp] + word[tmp2 + 1:tmp] + word[tmp2] + word[tmp + 1:]


def testNGramEditDistance(x, n, path):
    def coeffJaccard(x_gram, y_gram):
        inter = 0
        for x in x_gram:
            if x in y_gram:
                inter += 1
        union = len(x_gram)
        for y in y_gram:
            if y not in x_gram:
                union += 1
        return 0 if union == 0 else float(inter) / float(union)

    def nGramEditDistance(x, n, path):
        x_gram = nGramMaker(x, n)
        CJ_minimo = 0.8
        minimoAttuale = [None, len(x), 0]
        paroleMinime = []
        f = open(path, 'r')

        for i in range(len(x_gram)):
            for word in f:
                word = word.rstrip()
                y_gram = nGramMaker(word, n)
                cj = coeffJaccard(x_gram, y_gram)
                if CJ_minimo < cj:
                    tmp = editDistance(x, word)
                    if tmp < minimoAttuale[1]:
                        paroleMinime = []
                        minimoAttuale[0] = word
                        minimoAttuale[1] = tmp
                        minimoAttuale[2] = cj
                        paroleMinime.append(minimoAttuale)
                    elif tmp == minimoAttuale[1]:
                        paroleMinime.append([word, tmp, cj])
        f.close()
        return paroleMinime

    def cost(operator):
        if operator in ["COPY"]:
            return 0
        if operator in ["TWIDDLE"]:
            return 1.25
        if operator in ["INSERT"]:
            return 1
        if operator in ["DELETE"]:
            return 1
        if operator in ["REPLACE"]:
            return 1

    def editDistance(x, y):
        m = len(x)
        n = len(y)
        c = [[float("inf") for i in range(n + 1)] for j in range(m + 1)]
        for i in range(0, m + 1):
            c[i][0] = i * cost("DELETE")
        for j in range(0, n + 1):
            c[0][j] = j * cost("INSERT")

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if x[i - 1] == y[j - 1]:
                    c[i][j] = c[i - 1][j - 1] + cost("COPY")
                else:
                    c[i][j] = c[i - 1][j - 1] + cost("REPLACE")
                if i >= 2 and j >= 2 and x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1] and c[i - 2][j - 2] + cost(
                        "TWIDDLE") < c[i][j]:
                    c[i][j] = c[i - 2][j - 2] + cost("TWIDDLE")
                if c[i - 1][j] + cost("DELETE") < c[i][j]:
                    c[i][j] = c[i - 1][j] + cost("DELETE")
                if c[i][j - 1] + cost("INSERT") < c[i][j]:
                    c[i][j] = c[i][j - 1] + cost("INSERT")
        return c[m][n]

    def nGramMaker(x, n):
        if x is None:
            return []
        a = [None] * (len(x) - n + 1)
        for i in range(len(x) - n + 1):
            a[i] = x[i:i + n]
        return a

    nGramEditDistance(x, n, path)


def testNormalEditDistance(x, file):
    def cost(operator):
        if operator in ["COPY"]:
            return 0
        if operator in ["TWIDDLE"]:
            return 1.25
        if operator in ["INSERT"]:
            return 1
        if operator in ["DELETE"]:
            return 1
        if operator in ["REPLACE"]:
            return 1

    def editDistance(x, y):
        m = len(x)
        n = len(y)
        c = [[float("inf") for i in range(n + 1)] for j in range(m + 1)]
        for i in range(0, m + 1):
            c[i][0] = i * cost("DELETE")
        for j in range(0, n + 1):
            c[0][j] = j * cost("INSERT")

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if x[i - 1] == y[j - 1]:
                    c[i][j] = c[i - 1][j - 1] + cost("COPY")
                else:
                    c[i][j] = c[i - 1][j - 1] + cost("REPLACE")
                if i >= 2 and j >= 2 and x[i - 1] == y[j - 2] and x[i - 2] == y[j - 1] and c[i - 2][j - 2] + cost(
                        "TWIDDLE") < c[i][j]:
                    c[i][j] = c[i - 2][j - 2] + cost("TWIDDLE")
                if c[i - 1][j] + cost("DELETE") < c[i][j]:
                    c[i][j] = c[i - 1][j] + cost("DELETE")
                if c[i][j - 1] + cost("INSERT") < c[i][j]:
                    c[i][j] = c[i][j - 1] + cost("INSERT")
        return c[m][n]

    def normalEditDistance(x, file):
        minimoAttuale = [None, len(x)]
        paroleMinime = []

        f = open(file, 'r')
        for word in f:
            word = word.rstrip()
            tmp = editDistance(x, word)
            if tmp < minimoAttuale[1]:
                paroleMinime = []
                minimoAttuale[0] = word
                minimoAttuale[1] = tmp
                paroleMinime.append(minimoAttuale)

            elif tmp == minimoAttuale[1]:
                paroleMinime.append([word, tmp])

        f.close()
        return paroleMinime

    normalEditDistance(x, file)


def file_len(filename):
    f = open(filename, 'r')
    count = 0
    for line in f:
        if line != "\n":
            count += 1
    return count


def doGraph(name, y_variable, x_variable, length, dictionary):
    x = np.arange(length)
    plt.bar(x, height=y_variable)
    plt.xticks(x, x_variable)
    plt.ylabel('Seconds')
    plt.savefig(name + (dictionary.replace('.txt', '')).replace('Dictionary/', '') + '.png')
    plt.close()


if __name__ == "__main__":
    path = "Dictionary/"
    fileList = {path + f: file_len(path + f) for f in listdir(path) if isfile(join(path, f))}

    print("\n")
    for j in fileList:
        time = []
        single = 0
        for i in range(1, 5):
            word = getRandomWord(4 + i, j, fileList[j])
            t = Timer(lambda: testNormalEditDistance(word, j))
            single += t.timeit(number=1)
        print("Tempo Edit Distance senza N-Grams nel dizionario " + j + ": " + str(round(single / 5, 5)))

        for k in range(0, 4):
            tempo = 0
            for i in range(1, 5):
                word = getRandomWord(4 + i, j, fileList[j])
                t = Timer(lambda: testNGramEditDistance(word, k + 2, j))
                tempo += t.timeit(number=1)
            print(
                "Tempo Edit Distance Con " + str(k + 2) + "-Grams nel dizionario" + j + ": " + str(round(tempo / 5, 5)))
            time.append(tempo/5)

        doGraph("exerciseA_fold/ParolaNonModificataSoloGram_", time, ['2-Grams', '3-Grams', "4-Grams", "5-Grams"], 4, j)

        time.append(single/5)
        doGraph("exerciseA_fold/ParolaNonModificata_", time, ['2-Grams', '3-Grams', "4-Grams", "5-Grams", 'No Grams'],
                5, j)

        time = []
        single = 0
        for i in range(1, 5):
            word = getRandomWord(4 + i, j, fileList[j])
            t = Timer(lambda: testNormalEditDistance(swapCharacter(word), j))
            single += t.timeit(number=1)
        print("Tempo Edit Distance senza N-Grams con due lettere scambiate " + j + ": " + str(round(single / 5, 5)))

        for k in range(0, 4):
            tempo = 0
            for i in range(1, 5):
                word = getRandomWord(4 + i, j, fileList[j])
                t = Timer(lambda: testNGramEditDistance(swapCharacter(word), k+2, j))
                tempo += t.timeit(number=1)
            print("Tempo Edit Distance Con " + str(k + 2) + "-Grams con due lettere scambiate " + j + ": " + str(
                round(tempo / 5, 5)))
            time.append(tempo/5)

        doGraph("exerciseA_fold/LetteraScambiataSoloGram_", time, ['2-Grams', '3-Grams', "4-Grams", "5-Grams"], 4, j)

        time.append(single/5)
        doGraph("exerciseA_fold/LetteraScambiata_", time, ['2-Grams', '3-Grams', "4-Grams", "5-Grams", 'No Grams'], 5,
                j)

        time = []
        single = 0
        for i in range(1, 5):
            word = getRandomWord(4 + i, j, fileList[j])
            t = Timer(lambda: testNormalEditDistance(addCharacter(word), j))
            single += t.timeit(number=1)
        print("Tempo Edit Distance senza N-Grams con un carattere aggiunto " + j + ": " + str(round(single / 5, 5)))

        for k in range(0, 4):
            tempo = 0
            for i in range(1, 5):
                word = getRandomWord(4 + i, j, fileList[j])
                t = Timer(lambda: testNGramEditDistance(addCharacter(word), k+2, j))
                tempo += t.timeit(number=1)
            print("Tempo Edit Distance Con " + str(k + 2) + "-Grams con un carattere aggiunto " + j + ": " + str(
                round(tempo / 5, 5)))
            time.append(tempo/5)

        doGraph("exerciseA_fold/LetteraAggiuntaSoloGram_", time, ['2-Grams', '3-Grams', "4-Grams", "5-Grams"], 4, j)

        time.append(single/5)
        doGraph("exerciseA_fold/LetteraAggiunta_", time, ['2-Grams', '3-Grams', "4-Grams", "5-Grams", 'No Grams'], 5, j)

        time = []
        single = 0
        for i in range(1, 5):
            word = getRandomWord(4 + i, j, fileList[j])
            t = Timer(lambda: testNormalEditDistance(removeCharacter(word), j))
            single += t.timeit(number=1)
        print("Tempo Edit Distance senza N-Grams con un carattere rimosso " + j + ": " + str(round(single / 5, 5)))

        for k in range(0, 4):
            tempo = 0
            for i in range(1, 5):
                word = getRandomWord(4 + i, j, fileList[j])
                t = Timer(lambda: testNGramEditDistance(removeCharacter(word), k+2, j))
                tempo += t.timeit(number=1)
            print("Tempo Edit Distance Con " + str(k + 2) + "-Grams con un carattere rimosso " + j + ": " + str(
                round(tempo / 5, 5)))
            time.append(tempo/5)

        doGraph("exerciseA_fold/LetteraRimossaSoloGram_", time, ['2-Grams', '3-Grams', "4-Grams", "5-Grams"], 4, j)

        time.append(single/5)
        doGraph("exerciseA_fold/LetteraRimossa_", time, ['2-Grams', '3-Grams', "4-Grams", "5-Grams", 'No Grams'], 5, j)

        time = []
        word = ["Contemporaneo", "Procastinare", "Petaloso", "Googlare", "Eserciziario"]
        single = 0
        for i in range(1, 5):
            t = Timer(lambda: testNormalEditDistance(word[i], j))
            single += t.timeit(number=1)
        print("Tempo Edit Distance Senza N-Grams su Parola non appartenente al dizionario:" + j + " " + str(
            round(single / 5, 5)))

        for k in range(0, 4):
            tempo = 0
            for i in range(1, 5):
                t = Timer(lambda: testNGramEditDistance(word[i], k + 2, j))
                tempo += t.timeit(number=1)
            print("Tempo Edit Distance con " + str(
                k + 2) + "-NGram su Parola non appartenente al dizionario:" + j + " " + str(
                round(tempo / 5, 5)))
            time.append(tempo/5)

        doGraph("exerciseA_fold/ParolaNonAppartenenteSoloGram", time, ['2-Grams', '3-Grams', "4-Grams", "5-Grams"], 4,
                j)

        time.append(single/5)
        doGraph("exerciseA_fold/ParolaNonAppartenente", time, ['2-Grams', '3-Grams', "4-Grams", "5-Grams", 'No Grams'],
                5, j)

        print("\n")
