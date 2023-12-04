import re
import pandas as pd


"""
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""


def part1(aunts):
    sue = aunts[(aunts.children.isnull()) | (aunts.children.eq(3))]
    sue = sue[sue.perfumes.isnull() | sue.perfumes.eq(1)]
    sue = sue[sue.cats.isnull() | sue.cats.eq(7)]
    sue = sue[sue.samoyeds.isnull() | sue.samoyeds.eq(2)]
    sue = sue[sue.pomeranians.isnull() | sue.pomeranians.eq(3)]
    sue = sue[sue.akitas.isnull() | sue.akitas.eq(0)]
    sue = sue[sue.vizslas.isnull() | sue.vizslas.eq(0)]
    sue = sue[sue.goldfish.isnull() | sue.goldfish.eq(5)]
    sue = sue[sue.trees.isnull() | sue.trees.eq(3)]
    sue = sue[sue.cars.isnull() | sue.cars.eq(2)]
    print("Part 1 Sue:")
    print(sue)


def part2(aunts):
    sue = aunts[(aunts.children.isnull()) | (aunts.children.eq(3))]
    sue = sue[sue.perfumes.isnull() | sue.perfumes.eq(1)]
    sue = sue[sue.cats.isnull() | sue.cats.gt(7)]
    sue = sue[sue.samoyeds.isnull() | sue.samoyeds.eq(2)]
    sue = sue[sue.pomeranians.isnull() | sue.pomeranians.lt(3)]
    sue = sue[sue.akitas.isnull() | sue.akitas.eq(0)]
    sue = sue[sue.vizslas.isnull() | sue.vizslas.eq(0)]
    sue = sue[sue.goldfish.isnull() | sue.goldfish.lt(5)]
    sue = sue[sue.trees.isnull() | sue.trees.gt(3)]
    sue = sue[sue.cars.isnull() | sue.cars.eq(2)]
    print("Part 2 Sue:")
    print(sue)


# Sue 500: cats: 2, goldfish: 9, children: 8
def run(input):
    data = input.read().splitlines()

    aunts = pd.DataFrame()
    m = re.compile(r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)")
    for line in data:
        name, cat1, vcat1, cat2, vcat2, cat3, vcat3 = m.match(line).groups()
        aunts.at[name, cat1] = int(vcat1)
        aunts.at[name, cat2] = int(vcat2)
        aunts.at[name, cat3] = int(vcat3)
    part1(aunts)
    part2(aunts)
