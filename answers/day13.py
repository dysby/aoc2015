import networkx as nx
import matplotlib.pyplot as plt
from grave import plot_network
from itertools import permutations


def seat_persons(node_list, G):
    l_nds = len(node_list)
    max_happiness = 0
    max_happiness_perm = None
    for perm in permutations(node_list):
        total_happiness = 0
        for idx in range(l_nds - 1):
            total_happiness += G[perm[idx]][perm[idx + 1]]["happiness"]
            total_happiness += G[perm[idx + 1]][perm[idx]]["happiness"]
        total_happiness += G[perm[0]][perm[l_nds - 1]]["happiness"]
        total_happiness += G[perm[l_nds - 1]][perm[0]]["happiness"]
        # print(perm, total_happiness)
        if total_happiness > max_happiness:
            max_happiness = total_happiness
            max_happiness_perm = perm

    print(max_happiness, max_happiness_perm)


def run(input):
    instructions = input.read().splitlines()

    """
    Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 81 happiness units by sitting next to Carol.
    """
    G = nx.DiGraph()
    for step in instructions:
        words = step[:-1].split()
        name1 = words[0]
        gain_lose = words[2]
        happiness = words[3]
        if gain_lose == "gain":
            happiness = int(happiness)
        else:
            happiness = -(int(happiness))
        name2 = words[-1]
        G.add_edge(name1, name2, happiness=happiness)

    nds = G.nodes()
    seat_persons(nds, G)

    G.add_node("Helder")
    for n in nds:
        G.add_edge(n, "Helder", happiness=0)
        G.add_edge("Helder", n, happiness=0)

    nds = G.nodes()
    seat_persons(nds, G)

    # _, ax = plt.subplots()
    ## spring, kamada_kawai, shell, spectral
    # plot_network(G, layout="spring", ax=ax)
    # plt.show()


# python -m ipdb script.py
