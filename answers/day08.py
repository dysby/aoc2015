"""
--- Day 8: Matchsticks ---

"" is 2 characters of code (the two double quotes), but the string contains zero characters.
"abc" is 5 characters of code, but 3 characters in the string data.
"aaa\"aaa" is 10 characters of code, but the string itself contains six "a" characters and a single, escaped quote character, for a total of 7 characters in the string data.
"\x27" is 6 characters of code, but the string itself contains just one - an apostrophe ('), escaped using hexadecimal notation.
Santa's list is a file that contains many double-quoted string literals, one on each line. The only escape sequences used are \\ (which represents a single backslash), \" (which represents a lone double-quote character), and \\x plus two hexadecimal characters (which represents a single character with that ASCII code).

Disregarding the whitespace in the file, what is the number of characters of code for string literals minus the number of characters in memory for the values of the strings in total for the entire file?
"""


class StateMachine:
    chars_in_memory = 0
    chars_in_stringliterals = 0
    chars_in_encoding = 0

    def __init__(self, initialState):
        StateMachine.chars_in_memory = 0
        StateMachine.chars_in_stringliterals = 0
        StateMachine.chars_in_encoding = 0
        self.currentState = initialState
        self.currentState.run()

    # Template method:
    def runAll(self, inputs):
        for i in inputs:
            self.currentState = self.currentState.next(i)
            self.currentState.run()


class State:
    def run(self):
        assert 0, "run not implemented"

    def next(self, input):
        assert 0, "next not implemented"


class Enter(State):
    def run(self):
        pass

    def next(self, input):
        if input == '"':
            StateMachine.chars_in_stringliterals += 1
            StateMachine.chars_in_encoding += 3  # corresponde a encontrar "\"
            return StateMachine.normal
        else:
            raise ValueError


class Normal(State):
    def run(self):
        pass

    def next(self, input):
        if input == "\\":
            StateMachine.chars_in_stringliterals += 1
            StateMachine.chars_in_encoding += 2  # corresponde a encontrar \\
            return StateMachine.escape
        elif input == '"':
            StateMachine.chars_in_stringliterals += 1
            StateMachine.chars_in_encoding += 3  # corresponde a encontrar \"" no fim
            return StateMachine.exit
        else:
            StateMachine.chars_in_memory += 1
            StateMachine.chars_in_stringliterals += 1
            StateMachine.chars_in_encoding += 1
            return self


class Escape(State):
    def run(self):
        pass

    def next(self, input):
        if input in ("\\", '"'):
            StateMachine.chars_in_stringliterals += 1
            StateMachine.chars_in_encoding += 2  # corresponde a codificar \\\\ ou \\\"
            StateMachine.chars_in_memory += 1
            return StateMachine.normal
        elif input == "x":
            StateMachine.chars_in_stringliterals += 1
            StateMachine.chars_in_encoding += 1
            return StateMachine.escape_hex
        else:
            raise ValueError("Invalid input in Escape state")


class EscapeHex(State):
    def __init__(self):
        self.count_char = 0

    def run(self):
        pass

    def next(self, input):
        self.count_char += 1
        if self.count_char == 2:
            StateMachine.chars_in_stringliterals += 1
            StateMachine.chars_in_encoding += 1
            StateMachine.chars_in_memory += 1
            self.count_char = 0
            return StateMachine.normal
        else:
            StateMachine.chars_in_stringliterals += 1
            StateMachine.chars_in_encoding += 1
            return self


class Exit(State):
    def run(self):
        pass

    def next(self, input):
        raise RuntimeError("Input not supported for Exit state")


StateMachine.enter = Enter()
StateMachine.normal = Normal()
StateMachine.escape = Escape()
StateMachine.escape_hex = EscapeHex()
StateMachine.exit = Exit()


def run(input):
    data = input.read().splitlines()

    chars_in_stringliterals = []
    chars_in_memory = []
    chars_in_encoding = []
    for line in data:
        machine = StateMachine(StateMachine.enter)
        machine.runAll(line)
        chars_in_stringliterals.append(StateMachine.chars_in_stringliterals)
        chars_in_encoding.append(StateMachine.chars_in_encoding)
        chars_in_memory.append(StateMachine.chars_in_memory)

    answer1 = sum(map(lambda x, y: x - y, chars_in_stringliterals, chars_in_memory))
    answer2 = sum(map(lambda x, y: x - y, chars_in_encoding, chars_in_stringliterals))
    print("Dif of chars Literals to Memory = ", answer1)
    print("Dif of chars Encoding to Literals = ", answer2)

