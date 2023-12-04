from collections import Counter
from tqdm import tqdm
from functools import partial
from multiprocessing.pool import Pool
import threading


def backup():
    final = 0
    for step in range(1, final + 1):
        houses = Counter()
        for house in range(1, step + 1):
            houses[house] += sum(
                map(
                    lambda elf: 10 * elf,
                    [elf for elf in range(1, step + 1) if house % elf == 0],
                )
            )
        print(houses.most_common(1))
        if max(houses) >= final:
            min_house = min(list(k for k, v in houses.items() if v > final))
            print(f"Minimum house receiving at least {final} presents is = {min_house}")
            break


house_presents = lambda house: sum(
    [elf * 10 for elf in range(1, house + 1) if house % elf == 0]
)

house_presents2 = lambda house: sum(
    [elf * 11 for elf in range(1, house + 1) if house % elf == 0 and house <= elf * 50]
)


def binary_search(target):
    """
    https://en.wikipedia.org/wiki/Binary_search_algorithm
    Procedure for finding the leftmost element
    """
    left = 0
    right = target
    while left < right:
        m = int(right - (right - left) / 2)
        presents = house_presents(m)
        print(f"l={left} m={m} p={presents} r={right}")
        if presents < target:
            left = m + 1
        else:
            right = m
    return left


min_house = 29000000

house_lock = threading.Lock()


def test_house(house):
    final = 29000000
    presents = house_presents(house)
    if presents >= final:
        print(
            f"Minimum house receiving at least {final} presents is = {house} with {presents}"
        )
        with house_lock:
            if min_house > presents:
                min_house = presents
        # return (True, house, presents)
    # else:
    # return (False, house, presents)


def test_house2(house):
    final = 29000000
    presents = house_presents2(house)
    if presents >= final:
        print(
            f"Minimum house2 receiving at least {final} presents is = {house} with {presents}"
        )
        with house_lock:
            if min_house > presents:
                min_house = presents


def run(input):
    final = int(input.read().strip())
    # house = binary_search(final)
    # print(house)
    start = 650000
    end = 750000
    print(start, house_presents(start))
    print(start, house_presents2(start))

    tqdm.get_lock()  # ensures locks exist
    p = Pool(6)
    list(tqdm(p.imap(test_house2, range(start, end + 1)), total=(end - start)))
    p.close()
    print(min_house)

    """
    with Pool(6) as pool:
        # reached, house, presents = pool.map(test_house, range(start, end + 1))
        # print(reached, house, presents)
        pool.map(test_house2, range(start, end + 1))
    print(min_house)
   
    # other
    for house in tqdm(range(start, final + 1)):
        presents = house_presents(house)
        if presents >= final:
            print(
                f"Minimum house receiving at least {final} presents is = {house} with {presents}"
            )
            break
    """
