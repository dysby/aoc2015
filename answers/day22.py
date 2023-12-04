import re
import random
from itertools import combinations
from abc import abstractmethod
from copy import deepcopy


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
    def __init__(self, name):
        super().__init__(name)
        self.health = 50
        self.mana = 500
        self.mana_used = 0
        self.effects = []

    def cast(self, spell, boss):
        self.mana -= spell.cost
        self.mana_used += spell.cost

        if isinstance(spell, MagicMissile):
            boss.take_hit(spell.damage)
        elif isinstance(spell, Drain):
            boss.take_hit(spell.damage)
            self.health += spell.heals
        elif isinstance(spell, Poison):
            boss.effects.append(spell)
        elif isinstance(spell, (Shield, Recharge)):
            self.effects.append(spell)

    def __str__(self):
        return (
            f"Wizard {self.name}, h:{self.health}, m:{self.mana}, m_u:{self.mana_used}"
        )


class Boss(Character):
    def __init__(self, name, weapon_score, health):
        super().__init__(name)
        self.health = health
        self.damage = weapon_score
        self.defence = 0
        self.effects = []

    def __str__(self):
        return f"Boss {self.name}, bh:{self.health}"


"""
    def __repr__(self):
        return "{} ('{}') -> +{})".format(
            self.name, self.__class__.__name__, self.bonus
        )
"""


class Spell:
    """
    Magic Missile costs 53 mana. It instantly does 4 damage.

    Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.

    Shield costs 113 mana. It starts an effect that lasts for 6 turns.
    While it is active, your armor is increased by 7.

    Poison costs 173 mana. It starts an effect that lasts for 6 turns.
    At the start of each turn while it is active, it deals the boss 3 damage.

    Recharge costs 229 mana. It starts an effect that lasts for 5 turns.
    At the start of each turn while it is active, it gives you 101 new mana.
    """

    @property
    @abstractmethod
    def cost(self):
        raise NotImplementedError


class MagicMissile(Spell):
    def __init__(self):
        self.damage = 4
        self.timer = 0
        self.name = "MagicMissile"

    @property
    def cost(self):
        return 53


class Drain(Spell):
    def __init__(self):
        self.damage = 2
        self.heals = 2
        self.timer = 0
        self.name = "Drain"

    @property
    def cost(self):
        return 73


class Shield(Spell):
    def __init__(self):
        self.armor = 7
        self.timer = 6
        self.name = "Shield"

    @property
    def cost(self):
        return 113


class Poison(Spell):
    def __init__(self):
        self.damage = 3
        self.timer = 6
        self.name = "Poison"

    @property
    def cost(self):
        return 173


class Recharge(Spell):
    def __init__(self):
        self.mana = 101
        self.timer = 5
        self.name = "Recharge"

    @property
    def cost(self):
        return 229


SPELLS_LIST = [MagicMissile, Drain, Poison, Shield, Recharge]


def apply_effects(player, boss):
    # reset player armor
    player.defence = 0

    for effect in player.effects:
        if isinstance(effect, Shield):
            player.defence = effect.armor
        elif isinstance(effect, Recharge):
            player.mana += effect.mana
        effect.timer -= 1
    player.effects = [effect for effect in player.effects if effect.timer > 0]

    for effect in boss.effects:
        if isinstance(effect, Poison):
            boss.take_hit(effect.damage)
        effect.timer -= 1
    boss.effects = [effect for effect in boss.effects if effect.timer > 0]


def apply_spell(spell, player, boss):
    if isinstance(spell, MagicMissile):
        boss.take_hit(spell.damage)
    elif isinstance(spell, Drain):
        boss.take_hit(spell.damage)
        player.health += spell.heals
    elif isinstance(spell, Poison):
        boss.effects.append(spell)
    elif isinstance(spell, (Shield, Recharge)):
        player.effects.append(spell)


def generate_spell_strategy(mana_available, active_spells):
    """ Breath first search """

    for spell_cls in SPELLS_LIST:
        spell = spell_cls()
        if spell.cost <= mana_available and not isinstance(spell, active_spells):
            return spell


def all_valid_spells(mana_available, active_spells):

    valid_spells = []
    for spell_cls in SPELLS_LIST:
        spell = spell_cls()
        if spell.cost <= mana_available and not isinstance(spell, active_spells):
            valid_spells.append(spell)

    return valid_spells


# implementar o breath first algoritm para procurar todas as ações
# HTTP://CODE.ACTIVESTATE.COM/RECIPES/579138/
class Node(object):
    def __init__(self, id_, spell, player, boss):
        self.id = id_
        self.spell = spell
        self.player = player
        self.boss = boss
        self.children = []

    def __repr__(self):
        return f"Node: {self.id} -> {self.player.health} {self.boss.health}"

    def add_child(self, node):
        self.children.append(node)

    def get_children(self):
        return self.children

    def get_rev_children(self):
        children = self.children[:]
        children.reverse()
        return children


def get_breadth_first_nodes(root):
    nodes = []
    stack = [root]
    while stack:
        cur_node = stack[0]
        stack = stack[1:]
        nodes.append(cur_node)
        for child in cur_node.get_children():
            stack.append(child)
    return nodes


def get_depth_first_nodes(root):
    nodes = []
    stack = [root]
    while stack:
        cur_node = stack[0]
        stack = stack[1:]
        nodes.append(cur_node)
        for child in cur_node.get_rev_children():
            stack.insert(0, child)
    return nodes


def fight_tree(player, boss, hard):

    least_mana = 10000000  # infinity

    root = current_step = Node("root", None, player, boss)
    stack = [root]
    while stack:
        current_step = stack.pop()
        print(current_step.id, least_mana)

        current_player_spell_types = [
            effect.__class__ for effect in current_step.player.effects
        ]
        current_boss_spell_types = [
            effect.__class__ for effect in current_step.boss.effects
        ]

        for step_spell in all_valid_spells(
            current_step.player.mana,
            (*current_player_spell_types, *current_boss_spell_types),
        ):
            # copy Player and Boss from parent
            step_player = deepcopy(current_step.player)
            # step_player = Player(current_step.player.name)
            # step_player.damage = current_step.player.damage
            # step_player.defence = current_step.player.defence
            # step_player.effects = [e for e in current_step.player.effects]
            # step_player.health = current_step.player.health
            # step_player.mana = current_step.player.mana
            # step_player.mana_used = current_step.player.mana_used
            step_boss = deepcopy(current_step.boss)
            # step_boss = Boss(
            #     current_step.boss.name,
            #     current_step.boss.damage,
            #     current_step.boss.health,
            # )
            # step_boss.effects = [e for e in current_step.boss.effects]

            if hard:
                step_player.health -= 1
                if step_player.health <= 0:
                    current_step.add_child(
                        Node(
                            current_step.id + step_spell.name[0],
                            step_spell,
                            step_player,
                            step_boss,
                        )
                    )
                    # print("Boss Vitory")
                    # print(step_spell.name, step_player, step_boss)
                    continue

            # do turns
            # player cast spell
            step_player.cast(step_spell, step_boss)

            if step_boss.health <= 0:
                current_step.add_child(
                    Node(
                        current_step.id + step_spell.name[0],
                        step_spell,
                        step_player,
                        step_boss,
                    )
                )
                # print("Player Vitory")
                # print(step_spell.name, step_spell, step_player, step_boss)
                # vitoria
                if least_mana >= step_player.mana_used:
                    least_mana = step_player.mana_used
                continue

            # shortcut sabemos que será menor que 1600A
            if hard:
                if step_player.mana_used > 1216:
                    continue
            else:
                if step_player.mana_used > 974:
                    continue

            # boss turn
            # apply efects
            apply_effects(step_player, step_boss)
            if step_boss.health <= 0:
                current_step.add_child(
                    Node(
                        current_step.id + step_spell.name[0],
                        step_spell,
                        step_player,
                        step_boss,
                    )
                )
                # print("Player Vitory")
                # print(step_spell.name, step_player, step_boss)
                # vitoria
                if least_mana >= step_player.mana_used:
                    least_mana = step_player.mana_used
                continue
            # boss hit player
            step_player.take_hit(step_boss.damage)
            if step_player.health <= 0:
                current_step.add_child(
                    Node(
                        current_step.id + step_spell.name[0],
                        step_spell,
                        step_player,
                        step_boss,
                    )
                )
                # print("Boss Vitory")
                # print(step_spell.name, step_player, step_boss)
                continue

            # 1ª parte da player turn
            # apply effects
            apply_effects(step_player, step_boss)
            if step_boss.health <= 0:
                current_step.add_child(
                    Node(
                        current_step.id + step_spell.name[0],
                        step_spell,
                        step_player,
                        step_boss,
                    )
                )
                # print("Player Vitory")
                # print(step_spell.name, step_player, step_boss)
                # vitoria
                if least_mana >= step_player.mana_used:
                    least_mana = step_player.mana_used
                continue

            # append to move tree
            new_step = Node(
                current_step.id + step_spell.name[0], step_spell, step_player, step_boss
            )
            current_step.add_child(new_step)
            stack.append(new_step)

    print(f"least mana that still wins = {least_mana}")
    return root


def run(input):
    data = input.read()
    boss_properties = list(map(lambda x: int(x), re.findall(r"(\d+)", data)))
    player = Player("Helder")
    boss = Boss("Ogre", boss_properties[1], boss_properties[0])

    # _ = fight_tree(player, boss, hard=False)

    player = Player("Helder Hard")
    boss = Boss("Ogre", boss_properties[1], boss_properties[0])
    _ = fight_tree(player, boss, hard=True)

