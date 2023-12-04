"""
Sprinkles: capacity 5, durability -1, flavor 0, texture 0, calories 5
PeanutButter: capacity -1, durability 3, flavor 0, texture 0, calories 1
Frosting: capacity 0, durability -1, flavor 4, texture 0, calories 6
Sugar: capacity -1, durability 0, flavor 0, texture 2, calories 8
"""
import pandas as pd
import numpy as np
from itertools import product
import json
import os
from tqdm import tqdm


def t_sum100(i, j, k, l):
    if sum(i, j, k, l) == 100:
        return [i, j, k, l]


def generate_all_combinations(amount=100):
    # bag = [ele for ele in product(range(0, amount), repeat=4) if sum(ele) == amount]
    bag = []
    if os.path.isfile("data/cache15.json"):
        print("read cache file")
        with open("data/cache15.json", "r") as f:
            bag = json.load(f)
    else:
        print("generating combinations")
        x = list(range(100))
        for i in tqdm(x):
            res = [
                list((i, *ele))
                for ele in product(range(1, 101), repeat=3)
                if sum(ele, i) == 100
            ]
            bag = bag + res

        with open("data/cache15.json", "w") as f:
            json.dump(bag, f)

    print(bag[0])
    return bag


def run(input):
    _ = input

    ref_names = ["Sprinkles", "PeanutButter", "Frosting", "Sugar"]

    ingredients = pd.DataFrame(
        {
            "capacity": [5, -1, 0, -1],
            "durability": [-1, 3, -1, 0],
            "flavor": [0, 0, 4, 0],
            "texture": [0, 0, 0, 2],
            "calories": [5, 1, 6, 8],
        },
        index=ref_names,
    )
    print(ingredients.head())

    recepies = generate_all_combinations()

    max_score = 0
    best_recepie = None
    best_500cal_recepie = None
    max_500cal_score = 0

    for recepie in tqdm(recepies):
        df = ingredients.mul(recepie, axis=0)
        df = df.sum(axis=0)
        df[df < 0] = 0
        score = df["capacity"] * df["durability"] * df["flavor"] * df["texture"]
        if score > max_score:
            max_score = score
            best_recepie = recepie
        if df["calories"] == 500:
            if score > max_500cal_score:
                best_500cal_recepie = recepie
                max_500cal_score = score

    print(f"max score {max_score} Recepie: {best_recepie}")
    print(f"500cal max score {max_500cal_score} Recepie: {best_500cal_recepie}")
    # recepies = pd.DataFrame(generate_all_combinations(), index=ref_names)
    # print(recepies.head())

