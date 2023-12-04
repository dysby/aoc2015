import re
from typing import Deque
import random
from itertools import combinations


class Character(object):
    def __init__(self, name):
        self.health = 100
        self.name = name
        self.defence = 0
        self.damage = 0

    def take_hit(self, damage):
        if self.defence > damage:
            self.health -= 1
        else:
            self.health = self.health - (damage - self.defence)


class Player(Character):
    def __init__(self, name, weapon, armor, rings):
        super().__init__(name)
        self.health = 100
        self._weapon = weapon
        self._armor = armor
        self._rings = rings

        atack_bonus = sum(
            ring.bonus for ring in self._rings if isinstance(ring, AtackRing)
        )
        self.damage = weapon.bonus + atack_bonus

        defence_bonus = armor.bonus if armor is not None else 0
        defence_bonus += sum(
            ring.bonus for ring in self._rings if isinstance(ring, DefenceRing)
        )
        self.defence = defence_bonus

    def cost(self):
        amount = self._weapon.cost
        amount += self._armor.cost if self._armor else 0
        amount += sum(ring.cost for ring in self._rings)
        return amount

    def __str__(self):
        rings = ",".join([ring.name for ring in self._rings])
        weapon = self._weapon.name
        armor = self._armor.name if self._armor is not None else ""
        return f"{self.name} is wearing a {armor}, wilding a {weapon} and {rings}"


class Boss(Character):
    def __init__(self, name, weapon_score, armor_score, health):
        super().__init__(name)
        self.health = health
        self.damage = weapon_score
        self.defence = armor_score


class Item:
    def __init__(self, name, cost, bonus):
        self.cost = cost
        self.name = name
        self.bonus = bonus

    def __repr__(self):
        """Returns representation of the object"""
        return "{} ('{}') -> +{})".format(
            self.name, self.__class__.__name__, self.bonus
        )


class Ring(Item):
    pass


class AtackRing(Ring):
    pass


class DefenceRing(Ring):
    pass


class Armor(Item):
    pass


class Weapon(Item):
    pass


def generate_all_from_store():
    shop = Shop()
    for w in shop.weapons:
        for a in shop.armors:
            for rs in combinations(shop.rings, 2):
                bag = {"weapon": w, "armor": a, "rings": rs}
                # print(bag)
                yield bag


def fight(player, boss):
    while True:
        boss.take_hit(player.damage)
        if boss.health <= 0:
            return player
        player.take_hit(boss.damage)
        if player.health <= 0:
            return boss


class Shop:
    def __init__(self):
        self.weapons = [
            Weapon("Dagger", 8, 4),
            Weapon("Shortsword", 10, 5),
            Weapon("Warhammer", 25, 6),
            Weapon("Longsword", 40, 7),
            Weapon("Greataxe", 74, 8),
        ]

        self.armors = [
            Armor("Leather", 13, 1),
            Armor("Chainmail", 31, 2),
            Armor("Splintmail", 53, 3),
            Armor("Bandedmail", 75, 4),
            Armor("Platemail", 102, 5),
            Armor("Fake", 0, 0),
        ]

        self.rings = [
            AtackRing("Damage +1", 25, 1),
            AtackRing("Damage +2", 50, 2),
            AtackRing("Damage +3", 100, 3),
            DefenceRing("Defense +1", 20, 1),
            DefenceRing("Defense +2", 40, 2),
            DefenceRing("Defense +3", 80, 3),
            Ring("Fake", 0, 0),
            Ring("Fake", 0, 0),
        ]


def run(input):
    data = input.read()
    boss_properties = list(map(lambda x: int(x), re.findall(r"(\d+)", data)))
    # boss = Boss("Ogre", boss_properties[1], boss_properties[2], boss_properties[0])

    least_cost = 10000000  # infinity
    for bag in generate_all_from_store():
        player = Player("Helder", bag["weapon"], bag["armor"], bag["rings"])
        boss = Boss("Ogre", boss_properties[1], boss_properties[2], boss_properties[0])
        winner = fight(player, boss)
        if isinstance(winner, Player):
            cost = winner.cost()
            if cost < least_cost:
                least_cost = cost
                print(cost, winner)

    print(f"Least cost winner {least_cost}")

    most_cost = 0
    for bag in generate_all_from_store():
        player = Player("Helder", bag["weapon"], bag["armor"], bag["rings"])
        boss = Boss("Ogre", boss_properties[1], boss_properties[2], boss_properties[0])
        winner = fight(player, boss)
        if isinstance(winner, Boss):
            cost = player.cost()
            if cost > most_cost:
                most_cost = cost
                print(cost, player)

    print(f"Most cost looser {most_cost}")
