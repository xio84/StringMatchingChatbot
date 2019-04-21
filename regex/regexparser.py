import re
import heapq

from pip._vendor.distlib.compat import raw_input
from itertools import permutations


# i = raw_input("enter an input")
# seq = "cookiecrumbcola"
# print(re.findall(i,seq))
# re.match(i,seq)

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        self._index -= 1
        return heapq.heappop(self._queue)[-1]

    def size(self):
        return self._index

    @property
    def index(self):
        return self._index


def parsedata(filename):
    f = open(filename, "r")
    sw = open("stopwords.txt", "r")
    linesw = sw.readlines()
    line = f.readlines()
    db = []
    for x in line:
        entry = x.split("? ")
        entry[0] += "?"
        entry[0] = entry[0].split(". ")[1]
        for y in linesw:
            entry[0] = re.sub(r'\s?' + y.strip() + r'\s?', ' ', entry[0])
        db.append(entry)
    sw.close()
    return db


# def parseword(filename):
#     f = open(filename, "r")
#     line = f.readlines()
#     db = []
#     for x in line:
#         entry = x.split("? ")
#         entry[0] += "?"
#         entry[0] = entry[0].split(". ")[1]
#         entry[0] = entry[0].split(" ")
#         db.append(entry)
#     return db


def main(fn):
    db = parsedata(fn)
    regexin = raw_input("Masukkan query regex!")
    # matching synonyms
    s = open("sinonim.txt", "r")
    sline = s.readlines()
    for a in sline:
        aa = a.split(' : ')
        aa[1] = aa[1].strip()
        regexin = re.sub(aa[0], aa[1], regexin)
    # removing stopwords
    sw = open("stopwords.txt", "r")
    linesw = sw.readlines()
    for y in linesw:
        regexin = re.sub(r'\s?' + y.strip() + r'\s?', ' ', regexin)
    regexin = r'.*?' + regexin
    regexin = re.sub(' ', r'.*?', regexin)
    print(regexin)
    result = PriorityQueue()
    for x in db:
        y = re.match(regexin, x[0], re.I)
        if y is not None:
            z = len(y[0]) / len(x[0])
            result.push([x[1], z], z)
    # if result.size() == 0:
    # db = parseword(fn)
    # i = 0
    # while i < len(db):
    #     found = False
    #     word = ""
    #     while not found:
    #         fail = False
    #         j = 0
    #         while not fail and j<len(db[i][0]):
    #             temp = word + db[i][0][j] + " "
    #
    #         y = re.search(regexin, word)
    #         if y is not None:
    #             found = True
    #             z = len(y[0]) / len(word)
    #             result.push([db[i][1], z], z)
    #     i = i + 1
    #     print(i)
    return result


output = main("pertanyaan.txt")
print("Results:")
while output.index > 0:
    a = output.pop()
    print(a[0] + ", Match = " + str(a[1]))
