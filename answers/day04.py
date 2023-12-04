import hashlib


def find_hash_zeros(n, secret):
    zeros = "0" * n
    seed = 0

    while True:
        h = hashlib.md5(f"{secret}{seed}".encode())
        hd = h.hexdigest()
        if hd[:n] == zeros:
            break
        seed += 1
    return seed


def run(input):
    secret = input.read().strip()

    answer_1 = find_hash_zeros(5, secret)
    answer_2 = find_hash_zeros(6, secret)

    print(answer_1, answer_2)
