from collections import Counter


def move(x, y, c):
    if c == "^":
        y += 1
    elif c == "v":
        y -= 1
    elif c == "<":
        x -= 1
    elif c == ">":
        x += 1
    return x, y


def run(input):
    data = input.read()

    x, y = 0, 0
    houses = Counter({"0,0": 1})
    for c in data:
        x, y = move(x, y, c)
        houses[f"{x},{y}"] += 1

    answer = len(houses)

    x_santa, y_santa = 0, 0
    x_robot, y_robot = 0, 0
    houses_santa = Counter({"0,0": 1})
    houses_robot = Counter({"0,0": 1})
    for i, c in enumerate(data):
        if i % 2 == 0:
            x_robot, y_robot = move(x_robot, y_robot, c)
            houses_robot[f"{x_robot},{y_robot}"] += 1
        else:
            x_santa, y_santa = move(x_santa, y_santa, c)
            houses_santa[f"{x_santa},{y_santa}"] += 1

    houses_santa.update(houses_robot)
    answer_2 = len(houses_santa)

    print(answer, answer_2)
