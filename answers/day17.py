"""
containers of size 20, 15, 10, 5, and 5 liters
"""
import string
import random
from itertools import chain, combinations
from collections import Counter


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


class Container:
    def __init__(self, capacity):
        self.capacity = capacity
        self.name = Container.name_generator(5)

    def __repr__(self):
        return f"({self.name}) {self.capacity}"

    @staticmethod
    def name_generator(size):
        chars = string.ascii_lowercase
        return "".join(random.choice(chars) for _ in range(size))


def run(input):
    bottles = [Container(int(line)) for line in input.readlines()]
    lenCounter = Counter()
    count = 0
    for items in powerset(bottles):
        acc = sum(n.capacity for n in items)
        if acc == 150:
            count += 1
            lenCounter[len(items)] += 1

    minkey = min(lenCounter.keys())

    print(f"Total combinations = {count}")
    print("Min size combinations = ", lenCounter[minkey])
