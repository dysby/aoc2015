import itertools

# Passwords may not contain the letters i, o, or l
letters = "abcdefghijklmnopqrstuvwxyz"
valid_letters = "abcdefghjkmnpqrstuvwxyz"
doubles = [c * 2 for c in valid_letters]

_3lettersequences = (
    "abc",
    "bcd",
    "cde",
    "def",
    "efg",
    "fgh",
    "ghj",
    "hjk",
    "jkm",
    "kmn",
    "mnp",
    "npq",
    "pqr",
    "qrs",
    "rst",
    "stu",
    "tuv",
    "uvw",
    "vwx",
    "wxy",
    "xyz",
)


def next_letter(char):
    idx = letters.index(char) + 1
    if idx in (8, 11, 14):
        idx += 1
    caret = False
    # len(letters) = 26
    if idx == 26:
        idx = 0
        caret = True
    return caret, letters[idx]


def shiftpass(password):
    caret = True
    for idx in itertools.cycle(range(-1, -8, -1)):
        caret, new_letter = next_letter(password[idx])
        password = password[: 8 + idx] + new_letter + password[8 + idx + 1 :]
        if caret is not True:
            break
    return password


def validate(password: str) -> bool:
    """Return True if valid password"""
    valid_rule1 = False  # must have a 3 letter sequence
    for seq in _3lettersequences:
        if seq in password:
            valid_rule1 = True
            break
    if valid_rule1 is not True:
        return valid_rule1

    valid_rule2 = False  # must have a least two different double letter sequence
    for seq in doubles:
        if seq in password:
            for seq2 in [s for s in doubles if s != seq]:
                if seq2 in password:
                    valid_rule2 = True
                    break
            break

    return valid_rule1 and valid_rule2


def generate_password(data):
    password = data
    invalid = True
    while invalid:
        password = shiftpass(password)
        invalid = False if validate(password) else True
        # print(password)
    return password


def run(input):
    data = input.read().strip()
    new_password = generate_password(data)
    print(new_password)
