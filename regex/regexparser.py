import re
import heapq

from pip._vendor.distlib.compat import raw_input


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


def parsedata(filename):
    f = open(filename, "r")
    line = f.readlines()
    dict = []
    for x in line:
        entry = x.split("? ")
        entry[0] += "?"
        entry[0] = entry[0].split(". ")[1]
        dict.append(entry)
    return dict


def parseword(filename):
    f = open(filename, "r")
    line = f.readlines()
    dict = []
    for x in line:
        entry = x.split("? ")
        entry[0] += "?"
        entry[0] = entry[0].split(". ")[1]
        entry[0] = entry[0].split(" ")
        dict.append(entry)
    return dict


def main():
    fn = input("Masukkan nama file yang akan digunakan sebagai database!")
    dict = parsedata(fn)
    regexin = input("Masukkkan query regex!")
    result = PriorityQueue()
    for x in dict:
        y = re.search(regexin, x[0])
        if y is not None:
            z = len(x[0]) / len(y[0])
            result.push([x[1], z], z)
    return result


output = main()
print("Results:")
while output._index>0:
    a = output.pop()
    print(a[0] + ", Match = " + str(a[1]))
