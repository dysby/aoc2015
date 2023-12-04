import re

"""
hlf r
tpl r
inc r
jmp offset
jie r, offset
jio r, offset
"""


class Interpreter:
    a = 1
    b = 0
    ixp = 0
    expressions = [
        r"(hlf) (a|b)",
        r"(tpl) (a|b)",
        r"(inc) (a|b)",
        r"(jmp) ([+-]\d+)",
        r"(jie) (a|b), ([+-]\d+)",
        r"(jio) (a|b), ([+-]\d+)",
    ]

    def __init__(self, program):
        self.memory = program

    def run(self):
        for exp in self.step():
            print(f"{self.a}, {self.b}, {self.ixp}, {exp}")
            # input()
            for to_match in self.expressions:
                m = re.match(to_match, exp)
                if m:
                    method_name = m[1]
                    method = getattr(self, method_name)
                    method(m)
                    break

    def hlf(self, m):
        r = m[2]
        register = getattr(self, r)
        # register = register / 2
        setattr(self, r, register / 2)
        self.ixp += 1

    def tpl(self, m):
        r = m[2]
        register = getattr(self, r)
        setattr(self, r, register * 3)
        self.ixp += 1

    def inc(self, m):
        r = m[2]
        register = getattr(self, r)
        setattr(self, r, register + 1)
        self.ixp += 1

    def jmp(self, m):
        offset = int(m[2])
        self.ixp += offset

    def jie(self, m):
        r = m[2]
        offset = int(m[3])
        register = getattr(self, r)
        if register % 2 == 0:
            self.ixp += offset
        else:
            self.ixp += 1

    def jio(self, m):
        r = m[2]
        offset = int(m[3])
        register = getattr(self, r)
        if register == 1:
            self.ixp += offset
        else:
            self.ixp += 1

    def step(self):
        max_ixp = len(self.memory)
        while True:
            if self.ixp < max_ixp:
                yield self.memory[self.ixp]
            else:
                return


def run(input):
    data = input.readlines()

    interpreter = Interpreter(data)
    interpreter.run()
    print(f"Register b = {interpreter.b}")
