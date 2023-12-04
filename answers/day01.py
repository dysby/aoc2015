def run(input):
    data = input.read()

    answer_1 = 0  # floor 0
    for n in data:
        if n == "(":
            answer_1 += 1
        elif n == ")":
            answer_1 -= 1

    answer_2 = 0  # floor 0
    running = 0
    for n in data:
        if n == "(":
            running += 1
        elif n == ")":
            running -= 1
        answer_2 += 1
        if running == -1:
            break
    print(answer_1, answer_2)
