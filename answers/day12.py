import re
import json


def getValues(objs):
    value = 0
    if isinstance(objs, list):
        # Do this only for objects ({...}), not arrays ([...]).
        # if "red" in objs:
        #    return 0
        # else:
        for obj in objs:
            value += getValues(obj)
    elif isinstance(objs, dict):
        if "red" in objs.values():
            return 0
        else:
            for v in objs.values():
                value += getValues(v)
    elif isinstance(objs, int):
        # if objs < 0:
        #    print(objs)
        return objs
    else:
        # str, float, True, False, None
        return 0
    return value


def run(input):

    num = re.compile(r"(-?\d+)")

    data = input.read().strip()

    # heap = []
    # for c in re.findall(num, data):
    #    heap.append(int(c))
    heap = sum(map(lambda c: int(c), re.findall(num, data)))
    print("Answer part1:", heap)

    objs = json.loads(data)
    print("Answer part2:", getValues(objs))
    # print(sum(map(lambda c: int(c), re.findall(num, data)))
