import re
import itertools

"""
turn on 0,0 through 999,999 would turn on (or leave on) every light.
toggle 0,0 through 999,0 would toggle the first line of 1000 lights, 
turning off the ones that were on, and turning on the ones that were off.
turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.
"""


def run(input):
    instructions = input.read().splitlines()

    grid = [[False for x in range(1000)] for y in range(1000)]
    grid2 = [[False for x in range(1000)] for y in range(1000)]
    # print(grid)

    p = re.compile(r".*(on|off|toggle)\s(\d+),(\d+)\D+(\d+),(\d+)")
    for step in instructions:
        m = p.match(step)
        # print(step)
        # print(m)
        instruction, start_x, start_y, end_x, end_y = m.groups()
        # print(instruction, start_x, start_y, end_x, end_y)
        start_x = int(start_x)
        start_y = int(start_y)
        end_x = int(end_x)
        end_y = int(end_y)
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                if instruction == "on":
                    grid[x][y] = True
                    grid2[x][y] += 1
                elif instruction == "off":
                    grid[x][y] = False
                    if grid2[x][y] > 0:
                        grid2[x][y] -= 1
                elif instruction == "toggle":
                    grid[x][y] = not grid[x][y]
                    grid2[x][y] += 2

    lights = sum(itertools.chain(*grid))
    lights2 = sum(itertools.chain(*grid2))
    print(lights, lights2)
