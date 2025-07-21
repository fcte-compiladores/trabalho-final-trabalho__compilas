def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y
def div(x, y): return x / y
def eq(x, y): return x == y
def ne(x, y): return x != y
def gt(x, y): return x > y
def lt(x, y): return x < y
def ge(x, y): return x >= y
def le(x, y): return x <= y

bin_ops = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': div,
    '==': eq,
    '!=': ne,
    '>': gt,
    '<': lt,
    '>=': ge,
    '<=': le
}
