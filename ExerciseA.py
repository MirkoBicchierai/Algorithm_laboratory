import string
import random
from timeit import Timer

import matplotlib.pyplot as plt
import numpy as np


# noinspection PyUnboundLocalVariable
def getRandomWord(length):
    file = open("Dizionario.txt", 'r')
    n = random.randint(0, 60000)
    for i in range(0, n):
        tmp = file.readline()
    while len(tmp) != length:
        tmp = file.readline()
    return tmp


def addCharacter(word):
    tmp = random.randint(0, len(word))
    return word[:tmp] + random.choice(string.ascii_letters) + word[tmp:]


def removeCharacter(word):
    tmp = random.randint(0, len(word))
    return word[:tmp] + word[(tmp + 1):]


def swapCharacter(word):
    tmp = random.randint(0, len(word) - 1)
    tmp2 = random.randint(0, len(word) - 1)
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
    else:
        return swapCharacter(word)  # TODO REMOVE IT


def testNGramEditDistance(x, n):
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

    def nGramEditDistance(x, n):
        path = "Dizionario.txt"
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

    def cost(operator):  # TODO cambiare
        if operator in ["COPY"]:
            return 0
        if operator in ["TWIDDLE"]:
            return 1.25
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

    nGramEditDistance(x, n)


def testNormalEditDistance(x):
    def cost(operator):   # TODO cambiare
        if operator in ["COPY"]:
            return 0
        if operator in ["TWIDDLE"]:
            return 1.25
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

    def normalEditDistance(x):
        path = "Dizionario.txt"
        minimoAttuale = [None, len(x)]
        paroleMinime = []

        f = open(path, 'r')
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

    normalEditDistance(x)


f = open("RisultatiTest.txt", "w")

tempo = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNormalEditDistance(word))
    tempo += t.timeit(number=1)
f.write("Tempo Edit Distance Senza N-Grams su Parola nel Dizionario: " + str(round(tempo / 5, 5)) + "\n")

tempo2 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(word, 2))
    tempo2 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 2-Grams su Parola nel Dizionario: " + str(round(tempo2 / 5, 5)) + "\n")

tempo3 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(word, 3))
    tempo3 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 3-Grams su Parola nel Dizionario: " + str(round(tempo3 / 5, 5)) + "\n")

tempo4 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(word, 4))
    tempo4 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 4-Grams su Parola nel Dizionario: " + str(round(tempo4 / 5, 5)) + "\n")

tempo5 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(word, 5))
    tempo5 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 5-Grams su Parola nel Dizionario: " + str(round(tempo5 / 5, 5)) + "\n\n")

x = np.arange(5)
plt.bar(x, height=[tempo, tempo2, tempo3, tempo4, tempo5])
plt.xticks(x, ['No Grams', '2-Grams', '3-Grams', "4-Grams", "5-Grams"])
plt.ylabel('Seconds')
plt.savefig('ParolaNonModificata.png')
plt.close()

x = np.arange(4)
plt.bar(x, height=[tempo2, tempo3, tempo4, tempo5])
plt.xticks(x, ['2-Grams', '3-Grams', "4-Grams", "5-Grams"])
plt.ylabel('Seconds')
plt.savefig('ParolaNonModificataSoloGram.png')
plt.close()

tempo = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNormalEditDistance(swapCharacter(word)))
    tempo += t.timeit(number=1)
f.write("Tempo Edit Distance Senza N-Grams su Parola con due lettere scambiate: " + str(round(tempo / 5, 5)) + "\n")

tempo2 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(swapCharacter(word), 2))
    tempo2 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 2-Grams su Parola con due lettere scambiate: " + str(round(tempo2 / 5, 5)) + "\n")

tempo3 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(swapCharacter(word), 3))
    tempo3 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 3-Grams su Parola con due lettere scambiate: " + str(round(tempo3 / 5, 5)) + "\n")

tempo4 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(swapCharacter(word), 4))
    tempo4 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 4-Grams su Parola con due lettere scambiate: " + str(round(tempo4 / 5, 5)) + "\n")

tempo5 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(swapCharacter(word), 5))
    tempo5 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 5-Grams su Parola con due lettere scambiate: " + str(round(tempo5 / 5, 5)) + "\n\n")

x = np.arange(5)
plt.bar(x, height=[tempo, tempo2, tempo3, tempo4, tempo5])
plt.xticks(x, ['No Grams', '2-Grams', '3-Grams', "4-Grams", "5-Grams"])
plt.ylabel('Seconds')
plt.savefig('LetteraScambiata.png')
plt.close()

x = np.arange(4)
plt.bar(x, height=[tempo2, tempo3, tempo4, tempo5])
plt.xticks(x, ['2-Grams', '3-Grams', "4-Grams", "5-Grams"])
plt.ylabel('Seconds')
plt.savefig('LetteraScambiataSoloGram.png')
plt.close()

tempo = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNormalEditDistance(addCharacter(word)))
    tempo += t.timeit(number=1)
f.write("Tempo Edit Distance Senza N-Grams su Parola con un carattere aggiunto: " + str(round(tempo / 5, 5)) + "\n")

tempo2 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(addCharacter(word), 2))
    tempo2 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 2-Grams su Parola con un carattere aggiunto: " + str(round(tempo2 / 5, 5)) + "\n")

tempo3 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(addCharacter(word), 3))
    tempo3 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 3-Grams su Parola con un carattere aggiunto: " + str(round(tempo3 / 5, 5)) + "\n")

tempo4 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(addCharacter(word), 4))
    tempo4 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 4-Grams su Parola con un carattere aggiunto: " + str(round(tempo4 / 5, 5)) + "\n")

tempo5 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(addCharacter(word), 5))
    tempo5 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 5-Grams su Parola con un carattere aggiunto: " + str(round(tempo5 / 5, 5)) + "\n\n")

x = np.arange(5)
plt.bar(x, height=[tempo, tempo2, tempo3, tempo4, tempo5])
plt.xticks(x, ['No Grams', '2-Grams', '3-Grams', "4-Grams", "5-Grams"])
plt.ylabel('Seconds')
plt.savefig('LetteraAggiunta.png')
plt.close()

x = np.arange(4)
plt.bar(x, height=[tempo2, tempo3, tempo4, tempo5])
plt.xticks(x, ['2-Grams', '3-Grams', "4-Grams", "5-Grams"])
plt.ylabel('Seconds')
plt.savefig('LetteraAggiuntaSoloGram.png')
plt.close()

tempo = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNormalEditDistance(removeCharacter(word)))
    tempo += t.timeit(number=1)
f.write("Tempo Edit Distance Senza N-Grams su Parola con un carattere rimosso: " + str(round(tempo / 5, 5)) + "\n")

tempo2 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(removeCharacter(word), 2))
    tempo2 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 2-Grams su Parola con un carattere rimosso: " + str(round(tempo2 / 5, 5)) + "\n")

tempo3 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(removeCharacter(word), 3))
    tempo3 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 3-Grams su Parola con un carattere rimosso: " + str(round(tempo3 / 5, 5)) + "\n")

tempo4 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(removeCharacter(word), 4))
    tempo4 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 4-Grams su Parola con un carattere rimosso: " + str(round(tempo4 / 5, 5)) + "\n")

tempo5 = 0
for i in range(1, 5):
    word = getRandomWord(4 + i)
    t = Timer(lambda: testNGramEditDistance(removeCharacter(word), 5))
    tempo5 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 5-Grams su Parola con un carattere rimosso: " + str(round(tempo5 / 5, 5)) + "\n\n")

x = np.arange(5)
plt.bar(x, height=[tempo, tempo2, tempo3, tempo4, tempo5])
plt.xticks(x, ['No Grams', '2-Grams', '3-Grams', "4-Grams", "5-Grams"])
plt.ylabel('Seconds')
plt.savefig('LetteraTolta.png')
plt.close()

x = np.arange(4)
plt.bar(x, height=[tempo2, tempo3, tempo4, tempo5])
plt.xticks(x, ['2-Grams', '3-Grams', "4-Grams", "5-Grams"])
plt.ylabel('Seconds')
plt.savefig('LetteraToltaSoloGram.png')
plt.close()

word = ["Contemporaneo", "Procastinare", "Petaloso", "Googlare", "Eserciziario"]

tempo = 0
for i in range(1, 5):
    t = Timer(lambda: testNormalEditDistance(word[i]))
    tempo += t.timeit(number=1)
f.write(
    "Tempo Edit Distance Senza N-Grams su Parola non appartenente al dizionario: " + str(round(tempo / 5, 5)) + "\n")

tempo2 = 0
for i in range(1, 5):
    t = Timer(lambda: testNGramEditDistance(word[i], 2))
    tempo2 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 2-Grams su Parola non appartenente al dizionario: " + str(round(tempo2 / 5, 5)) + "\n")

tempo3 = 0
for i in range(1, 5):
    t = Timer(lambda: testNGramEditDistance(word[i], 3))
    tempo3 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 3-Grams su Parola non appartenente al dizionario: " + str(round(tempo3 / 5, 5)) + "\n")

tempo4 = 0
for i in range(1, 5):
    t = Timer(lambda: testNGramEditDistance(word[i], 4))
    tempo4 += t.timeit(number=1)
f.write("Tempo Edit Distance Con 4-Grams su Parola non appartenente al dizionario: " + str(round(tempo4 / 5, 5)) + "\n")

tempo5 = 0
for i in range(1, 5):
    t = Timer(lambda: testNGramEditDistance(word[i], 5))
    tempo5 += t.timeit(number=1)
f.write(
    "Tempo Edit Distance Con 5-Grams su Parola non appartenente al dizionario: " + str(round(tempo5 / 5, 5)) + "\n\n")

x = np.arange(5)
plt.bar(x, height=[tempo, tempo2, tempo3, tempo4, tempo5])
plt.xticks(x, ['No Grams', '2-Grams', '3-Grams', "4-Grams", "5-Grams"])
plt.ylabel('Seconds')
plt.savefig('ParolaNonNelDizionario.png')
plt.close()

x = np.arange(4)
plt.bar(x, height=[tempo2, tempo3, tempo4, tempo5])
plt.xticks(x, ['2-Grams', '3-Grams', "4-Grams", "5-Grams"])
plt.ylabel('Seconds')
plt.savefig('ParolaNonNelDizionarioSoloGram.png')
plt.close()
