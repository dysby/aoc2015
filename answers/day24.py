from itertools import combinations
from functools import reduce
from operator import itemgetter


def gen_group(presents, depth):
    size = len(presents)
    for step_size in range(1, size):
        for combination in combinations(presents, step_size):
            if depth == 2:
                if len(combination) == size:
                    yield set(combination), {}
            else:
                group1_sum = sum(combination)
                remainder_presentes = presents - set(combination)
                remainder_sum = sum(remainder_presentes)
                if depth == 0:
                    if remainder_sum % 2 == 0:
                        if group1_sum == (remainder_sum / 2):
                            yield set(combination), remainder_presentes
                else:
                    # depth == 1
                    if group1_sum == remainder_sum:
                        yield set(combination), remainder_presentes


def distribute(presents, depth):
    size = len(presents)
    for step_size in range(1, size):
        for combination in combinations(presents, step_size):
            group1_sum = sum(combination)
            remainder_presentes = presents - set(combination)
            remainder_sum = sum(remainder_presentes)
            if depth == 0:
                if group1_sum == (remainder_sum / 3):
                    yield set(combination), remainder_presentes
            elif depth == 1:
                if group1_sum == (remainder_sum / 2):
                    yield set(combination), remainder_presentes
            elif depth == 2:
                if group1_sum == remainder_sum:
                    yield set(combination), remainder_presentes
            else:
                if len(combination) == size:
                    yield set(combination), {}


def run(input):
    presents = [int(item.strip()) for item in input.readlines()]
    presents.reverse()
    # presents = {int(item.strip()) for item in input.readlines()}
    presents = set(presents)

    valid_groups = []
    min_group_size = 10000000  # infinity
    min_entanglement = 100000000000  # infinity
    found = False
    for group1, r1_presents in gen_group(presents, depth=0):
        if found:
            break
        group1_size = len(group1)
        entanglement = reduce(lambda x, y: x * y, group1)
        if group1_size <= min_group_size:
            if entanglement <= min_entanglement:
                for group2, group3 in gen_group(r1_presents, depth=1):
                    # for group3, _ in gen_group(r2_presents, depth=2):
                    # group3 = r2_presents
                    if sum(group1) == sum(group2) == sum(group3):
                        print(
                            "Combination 3 groups",
                            (group1_size, entanglement, group1, group2, group3),
                        )
                        valid_groups.append(
                            (group1_size, entanglement, group1, group2, group3)
                        )
                        # reduzir memoria e eliminar ramos que não interessam
                        if group1_size <= min_group_size:
                            min_group_size = group1_size
                        if entanglement <= min_entanglement:
                            min_entanglement = entanglement
                        found = True
                        break

    """
    # https://docs.python.org/3.8/library/operator.html#operator.itemgetter
    get_entanglement = itemgetter(1)
    get_size = itemgetter(0)

    valid_groups_size_sorted = sorted(valid_groups, key=get_size)
    min_size = get_size(valid_groups_size_sorted[0])
    only_min_size_valid_groups = filter(lambda x: get_size(x) == min_size, valid_groups)
    min_entanglement_attributes = sorted(
        only_min_size_valid_groups, key=get_entanglement
    )[0]

    print("Max group1 size combination", min_entanglement_attributes)
    """

    min_group_size = 10000000  # infinity
    min_entanglement = 100000000000  # infinity
    found = False
    for group1, r1_presents in distribute(presents, depth=0):
        if found:
            break
        group1_size = len(group1)
        entanglement = reduce(lambda x, y: x * y, group1)
        if group1_size <= min_group_size:
            if entanglement <= min_entanglement:
                for group2, r2_presents in distribute(r1_presents, depth=1):
                    for group3, group4 in distribute(r2_presents, depth=2):
                        if sum(group1) == sum(group2) == sum(group3) == sum(group4):
                            print(
                                "Combination 4 groups",
                                (
                                    group1_size,
                                    entanglement,
                                    group1,
                                    group2,
                                    group3,
                                    group4,
                                ),
                            )
                            # reduzir memoria e eliminar ramos que não interessam
                            if group1_size <= min_group_size:
                                min_group_size = group1_size
                            if entanglement <= min_entanglement:
                                min_entanglement = entanglement
                            found = True
                            break
                    break
