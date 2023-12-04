from itertools import starmap, product


SIZE = 100
STEPS = 100


def neighbors(grid, x, y):
    # neighbrs = starmap(lambda a, b: (x + a, y + b), product((0, -1, +1), (0, -1, +1)))
    # list(neighbrs)[:1] retira o (x, y) que é o primeiro elemento de neighbrs
    # state = [grid[a][b] for (a, b) in list(neighbrs)[1:]]
    X = SIZE - 1
    Y = SIZE - 1

    neighbors = [
        grid[y2][x2]
        for x2 in range(x - 1, x + 2)
        for y2 in range(y - 1, y + 2)
        if (
            -1 < x <= X
            and -1 < y <= Y
            and (x != x2 or y != y2)
            and (0 <= x2 <= X)
            and (0 <= y2 <= Y)
        )
    ]

    return neighbors


def step(grid):
    grid2 = [[False for x in range(SIZE)] for y in range(SIZE)]
    for x, y in product(range(SIZE), repeat=2):
        neighbrs_state = sum(neighbors(grid, x, y))
        # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
        if grid[y][x] == True:
            if neighbrs_state in (2, 3):
                grid2[y][x] = True
        # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
        else:
            if neighbrs_state == 3:
                grid2[y][x] = True
            # else stays off/False

    return grid2


def step2(grid):
    grid2 = [[False for x in range(SIZE)] for y in range(SIZE)]
    grid2[0][0] = True
    grid2[0][SIZE - 1] = True
    grid2[SIZE - 1][SIZE - 1] = True
    grid2[SIZE - 1][0] = True
    for x, y in product(range(SIZE), repeat=2):
        if (x, y) not in [(0, 0), (0, SIZE - 1), (SIZE - 1, SIZE - 1), (SIZE - 1, 0)]:
            neighbrs_state = sum(neighbors(grid, x, y))
            # A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
            if grid[y][x] == True:
                if neighbrs_state in (2, 3):
                    grid2[y][x] = True
            # A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
            else:
                if neighbrs_state == 3:
                    grid2[y][x] = True
                # else stays off/False

    return grid2


def run(input):
    grid = [[False for x in range(SIZE)] for y in range(SIZE)]

    grid2 = [[False for x in range(SIZE)] for y in range(SIZE)]
    grid2[0][0] = True
    grid2[0][SIZE - 1] = True
    grid2[SIZE - 1][SIZE - 1] = True
    grid2[SIZE - 1][0] = True

    for y, line in enumerate(input.readlines()):
        for x, c in enumerate(line.strip()):
            if c == "#":
                grid[y][x] = True
                grid2[y][x] = True

    # for y in range(SIZE):
    #     print("".join(map(lambda x: "#" if x is True else ".", grid[y])))
    for _ in range(STEPS):
        #     print("=================================")
        grid = step(grid)
        grid2 = step2(grid2)
    #     for y in range(SIZE):
    #         print("".join(map(lambda x: "#" if x is True else ".", grid[y])))

    lights = sum(
        starmap(
            lambda x, y: 1 if grid[x][y] is True else 0,
            list(product(range(SIZE), repeat=2)),
        )
    )
    lights2 = sum(
        starmap(
            lambda x, y: 1 if grid2[x][y] is True else 0,
            list(product(range(SIZE), repeat=2)),
        )
    )
    print("How many lights are on, answer1 ?", lights)
    print("How many lights are on, answer2 ?", lights2)
