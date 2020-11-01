from math import sqrt

ops = {"+":0, "-":0, "*":1, "/":1, "^":2, "(":3, ")":3}


class Operator:
    def __init__(self, op):
        self.op = op
        self.precedence = ops[self.op]

    def __repr__(self):
        if self.op in ("(", ")"):
            return f"Op({'LEFT' if self.op == '(' else 'RIGHT'})"
        return f"Op({self.op})"

    def exec(self, operand1, operand2):
        if self.op == "+":
            return operand1 + operand2
        elif self.op == "-":
           return operand1 - operand2
        elif self.op == "*":
            return operand1 * operand2
        elif self.op == "/":
            return operand1 / operand2
        elif self.op == "^":
            return operand1 ** operand2


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Var({self.name})"


class Number:
    def __init__(self, value):
        self.value = float(value)

    def __repr__(self):
        return f"Num({self.value})"


class Error:
    def __init__(self, absolute=None, relative=None, value=None):
        if absolute is None:
            self.absolute = value * relative
            self.relative = relative
            self.value = value
        elif relative is None:
            self.relative = absolute / value
            self.absolute = absolute
            self.value = value
        elif value is None:
            self.value = absolute / relative
            self.absolute = absolute
            self.relative = relative

    def __repr__(self):
        return f"{round(self.value, 4)} ±{round(self.absolute, 4)} ({round(self.relative*100, 4)}%)"

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Error(value=self.value + other,
                         absolute=self.absolute)
        else:
            return Error(value=self.value + other.value,
                         absolute=sqrt(self.absolute ** 2 + other.absolute ** 2))
    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Error(value=self.value - other,
                         absolute=self.absolute)
        else:
            return Error(value=self.value - other.value,
                         absolute=sqrt(self.absolute ** 2 + other.absolute ** 2))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Error(value=self.value * other,
                         relative=self.relative)
        else:
            return Error(value=self.value * other.value,
                         relative=sqrt(self.relative**2 + other.relative**2))
    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Error(value=self.value / other,
                         relative=self.relative)
        else:
            return Error(value=self.value / other.value,
                         relative=sqrt(self.relative**2 + other.relative**2))

    def __pow__(self, power):
        assert isinstance(power, (int, float))
        return Error(value=self.value ** power,
                     relative=self.relative * power)



def tokenise(expr):
    """Convert a mathematical expression as a string into a list of tokens for parsing"""
    expr = expr.replace(" ", "")
    out = []
    buffer = []
    for c in expr:
        if c in ops.keys():
            if len(buffer) != 0:
                out.append(Number("".join(buffer)))
                buffer = []
            out.append(Operator(c))
        elif c in map(str, range(10)):
            buffer.append(c)
        else:
            if len(buffer) != 0:
                out.append(Number("".join(buffer)))
                buffer = []
            out.append(Variable(c))
    if len(buffer) != 0:
        out.append(Number("".join(buffer)))
    return out


def convert_to_rpn(tokens):
    """Convert a list of tokens in infix order  to Reverse Polish Notation order"""
    out = []
    opstack = []
    for token in tokens:
        if isinstance(token, (Number, Variable)):
            out.append(token)
        elif isinstance(token, Operator) and (token.op not in ("(", ")")):
            while len(opstack) > 0 and opstack[-1].precedence >= token.precedence and opstack[-1].op != "(":
                out.append(opstack.pop())
            opstack.append(token)
        elif token.op == "(":
            opstack.append(token)
        elif token.op == ")":
            while opstack[-1].op != "(":
                out.append(opstack.pop())
                if len(opstack) == 0:
                    raise ValueError("Mismatched Brackets")
            opstack.pop()
    while len(opstack) != 0:
        out.append(opstack.pop())
    return out


def calculate_errors(expr, **errors):
    """Take an expression as a list of RPN tokens and a set of value,error pairs and calculate the final error"""
    stack = []
    for token in expr:
        if isinstance(token, Operator):
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = token.exec(operand1, operand2)
            stack.append(result)
        else:
            if isinstance(token, Variable):
                tostack = Error(value=errors[token.name][0],
                                absolute=errors[token.name][1])
            elif isinstance(token, Number):
                tostack = token.value
            stack.append(tostack)
    return stack[0]


def get_error(expr, **errors):
    return calculate_errors(convert_to_rpn(tokenise(expr)), **errors)


if __name__ == "__main__":
    e = "(x^2 + y^2) / (2*y)"
    c = get_error(e, x=(0.1, 0.0025), y=(0.01, 0.0025))
    print(c)
