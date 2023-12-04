from time import sleep


def cantor(x, y):
    if x == 1 and y == 1:
        return 20151125
    elif x == 1:
        return cantor(y - 1, 1)
    else:
        value = cantor(x - 1, y + 1) * 252533
        remainder = value % 33554393
        return remainder


def visit_cantor(x_end, y_end):
    x = 1
    y = 1
    last = 20151125
    while True:
        # print(f"({x}, {y}) = {last}")
        if x == x_end and y == y_end:
            return last

        if y == 1:
            y = x + 1
            x = 1
        else:
            x = x + 1
            y = y - 1
        last = (last * 252533) % 33554393


def run(input):

    data = input.read().split()

    input_row = int(data[15][:-1])
    input_column = int(data[17][:-1])
    # print(input_row, input_column)
    # sleep(3)
    # value = visit_cantor(input_row, input_column)
    value = visit_cantor(input_column, input_row)
    print(input_row, input_column, "\u2192", value)
