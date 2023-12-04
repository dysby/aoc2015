from functools import reduce


"""
(length l, width w, and height h)
"""


def surface_area(l, w, h):
    return 2 * l * w + 2 * w * h + 2 * h * l


def area_smallest_side(l, w, h):
    return min(l * w, l * h, w * h)


def shortest_distance_around(l, w, h):
    return 2 * min(l + w, l + h, w + h)


# def smallest_perimeter_face(l, w, h):
#    return 2*min(l+w, l+h, w+h)


def volume(l, w, h):
    return l * w * h


def dry(l, w, h, funcs):
    return reduce(lambda acc, y: acc + y, list(map(lambda x: x(l, w, h), funcs)))


def run(input):
    data = input.readlines()

    wrap = 0
    ribbon = 0
    funcs_wrap = [surface_area, area_smallest_side]
    funcs_ribbon = [shortest_distance_around, volume]
    for line in data:
        l, w, h = list(map(lambda i: int(i), line.split("x")))
        wrap += dry(l, w, h, funcs_wrap)
        ribbon += dry(l, w, h, funcs_ribbon)

    print(wrap, ribbon)
