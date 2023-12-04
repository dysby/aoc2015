import re


TT_SIGNAL = "TT_SIGNAL"
TT_AND = "TT_AND"
TT_OR = "TT_OR"
TT_RSHIFT = "TT_RSHIFT"
TT_LSHIFT = "TT_LSHIFT"
TT_NOT = "TT_NOT"
TT_ARROW = "TT_ARROW"
TT_IDENT = "TT_IDENT"


class Token:
    def __init__(self, _type, value):
        self.type = _type
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenizer(self):
        chars = re.compile(r"[a-zA-Z]+")
        decimals = re.compile(r"\d+")
        ops = re.compile(r"AND|OR|NOT|LSHIFT|RSHIFT")

        for token in self.text.split():
            if token == "->":
                yield Token(TT_ARROW, None)
            elif ops.match(token):
                if token == "AND":
                    op = Token(TT_AND, None)
                elif token == "OR":
                    op = Token(TT_OR, None)
                elif token == "NOT":
                    op = Token(TT_NOT, None)
                elif token == "LSHIFT":
                    op = Token(TT_LSHIFT, None)
                elif token == "RSHIFT":
                    op = Token(TT_RSHIFT, None)
                else:
                    raise ValueError
                yield op
            elif decimals.match(token):
                yield Token(TT_SIGNAL, int(token))
            elif chars.match(token):
                yield Token(TT_IDENT, token)


class Identifier:
    def __init__(self, lexeme):
        self.lexeme = lexeme


class Arrow:
    def __init__(self, lexeme):
        self.lexeme = lexeme


class Signal:
    def __init__(self, lexeme):
        self.lexeme = lexeme


class Operator:
    def __init__(self, lexeme):
        self.lexeme = lexeme

    @staticmethod
    def factory_build(lexeme):
        if lexeme == "AND":
            return And(lexeme)
        elif lexeme == "OR":
            return Or(lexeme)
        elif lexeme == "NOT":
            return Not(lexeme)
        elif lexeme == "LSHIFT":
            return Lshift(lexeme)
        elif lexeme == "RSHIFT":
            return Rshift(lexeme)


class And(Operator):
    def run(self, left, right):
        return left & right


class Or(Operator):
    def run(self, left, right):
        return left | right


class Not(Operator):
    def run(self, left, right):
        return ~right


class Lshift(Operator):
    def run(self, left, right):
        return left << right


class Rshift(Operator):
    def run(self, left, right):
        return left >> right


def tokenizer(line):
    chars = re.compile(r"[a-zA-Z]+")
    decimals = re.compile(r"\d+")
    ops = re.compile(r"AND|OR|NOT|LSHIFT|RSHIFT")

    for token in line.split():
        if token == "->":
            yield Arrow(token)
        elif ops.match(token):
            yield Operator.factory_build(token)
        elif decimals.match(token):
            yield Signal(token)
        elif chars.match(token):
            yield Identifier(token)


class AST:
    def _shift65536(self, v):
        if v < 0:
            return 65536 + v
        else:
            return v


class BinOptNode(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOpt:{self.op}"


class UniOptNode(AST):
    def __init__(self, op, right):
        self.right = right
        self.op = op

    def __repr__(self):
        return f"UniOpt:{self.op}"


class SignalNode(AST):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Signal:{self.value}"


class IdentNode(AST):
    def __init__(self, name, ast):
        self.name = name
        self.ast = ast

    def __repr__(self):
        return f"Identifier:{self.name}"


class ArrowNode(AST):
    def __init__(self, ast):
        self.ast = ast

    def __repr__(self):
        return f"Arrow: =>"


def to_16bitarray(n):
    return [n >> i & 1 for i in range(15, -1, -1)]


class Parser:
    def __init__(self, lexer):
        self.tokens = [t for t in lexer.tokenizer()]
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_token = self.tokens[self.tok_idx]
        return self.current_token

    def parse(self):
        res = self.expr()
        return res

    # factor : signal | ident | Not factor
    def factor(self):
        tok = self.current_token
        if tok.type == TT_SIGNAL:
            self.advance()
            return SignalNode(tok.value)
        elif tok.type == TT_IDENT:
            self.advance()
            return IdentNode(tok.value, None)
        else:
            return None

    def ufactor(self):
        tok = self.current_token
        if tok.type == TT_NOT:
            self.advance()
            factor = self.factor()
            return UniOptNode(tok, factor)
        return None

    # uterm : factor | Uni factor
    def uterm(self):
        left = self.factor() or self.ufactor()
        if left is None:
            raise ValueError
        return left

    # term : uterm (Opt uterm)*
    def term(self):
        # return self.bin_op(self.uterm, (TT_AND, TT_OR, TT_LSHIFT, TT_RSHIFT))
        left = self.uterm()
        while self.current_token.type in (TT_AND, TT_OR, TT_LSHIFT, TT_RSHIFT):
            opt = self.current_token
            self.advance()
            right = self.uterm()
            left = BinOptNode(left, opt, right)
        return left

    # expr : (factor|Uni factor) (Opt (factor|Uni factor))* arrow ident
    #
    # uterm : factor | Uni factor
    # expr : uterm (Opt uterm)* arrow ident
    #
    # term : uterm (Opt uterm)*
    # uterm : factor | Uni factor
    # expr : term arrow ident
    def expr(self):
        left = self.term()
        if self.current_token.type == TT_ARROW:
            self.advance()
            if self.current_token.type == TT_IDENT:
                ident = self.factor()
                ident.ast = left
            return ident
        else:
            raise ValueError

    def bin_op(self, func, ops):
        left = func()
        while self.current_token.type in ops:
            opt = self.current_token
            self.advance()
            right = func()
            left = BinOptNode(left, opt, right)
        return left


class Interpreter:
    def __init__(self, circuits):
        self.circuits = circuits

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_IdentNode(self, node):
        # print("found IdentNode", node.name)
        n = self.circuits[node.name]
        if n is not None:
            if n["value"] == "a":
                new_value = self.visit(n["ast"])
                n["value"] = new_value
                return new_value
            else:
                return n["value"]
        else:
            print("Ident empty")

    def visit_SignalNode(self, node):
        # print("found SignalNode")
        return node.value

    def visit_BinOptNode(self, node):
        # print("found BinOptNode")
        left = self.visit(node.left)
        right = self.visit(node.right)
        if node.op.type == TT_AND:
            result = left & right
        elif node.op.type == TT_OR:
            result = left | right
        elif node.op.type == TT_RSHIFT:
            result = left >> right
        elif node.op.type == TT_LSHIFT:
            result = left << right

        return self._shift65536(result)

    def visit_UniOptNode(self, node):
        # it can be only NOT
        # print("found UniOptNode")
        right = self.visit(node.right)
        return self._shift65536(~right)

    m16 = lambda x: x & 0xFFFF

    def _shift65536(self, v):
        if v < 0:
            return 65536 + v
        elif v > 65536:
            return v - 65536
        else:
            return v


def ast_print(i, node):
    lig = "L   " if i > 1 else ""
    if isinstance(node, IdentNode):
        print("    " * i, lig, node)
        print("    " * i, lig, "|")
        ast_print(i + 1, node.ast)
    elif isinstance(node, BinOptNode):
        print("    " * i, lig, node.op)
        print("    " * i, lig, "|")
        ast_print(i + 1, node.left)
        ast_print(i + 1, node.right)
    elif isinstance(node, SignalNode):
        print("    " * i, lig, node)
    elif isinstance(node, UniOptNode):
        print("    " * i, lig, node)
        print("    " * i, lig, "|")
        ast_print(i + 1, node.right)
    else:
        print("    " * i, "EOF")


def run(input):
    data = input.read().splitlines()

    circuits = {}
    for line in data:
        lexer = Lexer(line)
        parser = Parser(lexer)
        ident = parser.parse()
        # cada linha representa uma expressão (ident.ast => ident.name)
        # que é guardada no dicionario circuits
        circuits[ident.name] = {"ast": ident.ast, "value": "a"}

    interpreter = Interpreter(circuits)

    k = "a"
    answer = interpreter.visit(circuits[k]["ast"])
    print("Answer is:", k, "=>", answer)
    """
    for k in circuits.keys():
        answer = interpreter.visit(circuits[k]["ast"])
        # print("Answer is:", test, "=>", answer)
        print("Answer is:", k, "=>", answer)
    """
