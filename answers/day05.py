from collections import Counter

"""
A nice string is one with all of the following properties:

It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd),
or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one 
of the other requirements.
"""


def is_nice_string1(line):
    exclude = set(["ab", "cd", "pq", "xy"])
    vowels = set(["a", "e", "i", "o", "u"])
    is_nice = False

    c_vowels = 0
    double_letter = False
    have_exclude = False
    for i, c in enumerate(line):
        if c in vowels:
            c_vowels += 1
        if i > 0:
            if line[i - 1] == line[i]:
                double_letter = True
            if line[i - 1 : i + 1] in exclude:
                have_exclude = True
                break
    # print(c_vowels, double_letter, have_exclude)
    if not have_exclude and c_vowels > 2 and double_letter:
        is_nice = True
    return is_nice


"""
a nice string is one with all of the following properties:

It contains a pair of any two letters that appears at least twice in the 
string without overlapping, like xyxy (xy) or aabcdefgaa (aa), 
but not like aaa (aa, but it overlaps).
It contains at least one letter which repeats with exactly one letter between them,
like xyx, abcdefeghi (efe), or even aaa.
"""


def is_nice_string2(line):
    have_repeated_letter = False
    have_pair = False

    dups = Counter()
    # for i, k in enumerate(zip(line[0::2], line[1::2])):
    #    k_str = ''.join(k)
    #    #print(k_str, line[i*2+2:])
    #    if k_str in line[i*2+2:]: dups[k_str] += 1

    for i in range(0, len(line) - 2):
        if line[i : i + 2] in line[i + 2 :]:
            dups[f"{line[i:i+2]}"] += 1
    # print(dups)

    # c_dups = len([k for k, v in dups.items() if v > 1])
    # if c_dups > 0: have_pair=True
    if len(dups) > 0:
        have_pair = True
    # have_pair = True if len(dups) > 0 else False

    for i in range(2, len(line)):
        # print(line[i],line[i-2])
        if line[i] == line[i - 2]:
            have_repeated_letter = True
            break
    return have_pair and have_repeated_letter


def run(input):
    data = input.read().splitlines()

    answer_1 = 0
    answer_2 = 0

    for line in data:
        if is_nice_string1(line):
            answer_1 += 1
        if is_nice_string2(line):
            answer_2 += 1

    print(answer_1, answer_2)
