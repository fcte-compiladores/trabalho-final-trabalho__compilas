from typing import List, Callable, Optional, Union
from dataclasses import dataclass

Value = bool | int | float | None

@dataclass
class Expr:
    """Classe base para expressões."""

@dataclass
class Stmt:
    """Classe base para comandos."""

@dataclass
class BreakSignal:
    pass

class ReturnSignal:
    def __init__(self, value):
        self.value = value

@dataclass
class Var(Expr):
    name: str

    def eval(self, ctx):
        return ctx.get(self.name)

@dataclass
class Literal(Expr):
    value: Value

    def eval(self, ctx):
        return self.value

@dataclass
class BinOp(Expr):
    left: Expr
    right: Expr
    op: Callable[[Value, Value], Value]

    def eval(self, ctx):
        return self.op(self.left.eval(ctx), self.right.eval(ctx))

@dataclass
class Print(Stmt):
    expr: Expr

    def eval(self, ctx):
        print(self.expr.eval(ctx))

@dataclass
class ExprStmt(Stmt):
    expr: Expr

    def eval(self, ctx):
        self.expr.eval(ctx)

@dataclass
class Break(Stmt):
    def eval(self, ctx):
        return BreakSignal()

@dataclass
class Assign(Expr):
    name: str
    value: Expr

    def eval(self, ctx):
        val = self.value.eval(ctx)
        try:
            tipo_esperado = ctx.get_type(self.name)
        except NameError:
            raise NameError(f"Variável '{self.name}' não declarada.")
        if not check_type(tipo_esperado, val):
            raise TypeError(f"Tipo incorreto na atribuição para '{self.name}': esperado {tipo_esperado}, recebeu {type(val).__name__}")
        ctx.set_var(self.name, val)
        return val

@dataclass
class VarDef(Stmt):
    name: str
    value: Expr
    type: str

    def eval(self, ctx):
        val = self.value.eval(ctx)
        if not check_type(self.type, val):
            raise TypeError(f"Tipo incorreto para variável '{self.name}': esperado {self.type}, recebeu {type(val).__name__}")
        ctx.var_def(self.name, self.type, val)

@dataclass
class Block(Stmt):
    stmts: list[Stmt]

    def eval(self, ctx):
        for stmt in self.stmts:
            if stmt is None:
                continue
            result = stmt.eval(ctx)
            if isinstance(result, (BreakSignal, ReturnSignal)):
                return result
        return None

@dataclass
class If(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Optional[Stmt]

    def eval(self, ctx):
        if self.condition.eval(ctx):
            result = self.then_branch.eval(ctx)
            if isinstance(result, (BreakSignal, ReturnSignal)):
                return result
        elif self.else_branch:
            result = self.else_branch.eval(ctx)
            if isinstance(result, (BreakSignal, ReturnSignal)):
                return result

@dataclass
class While(Stmt):
    condition: Expr
    body: Stmt

    def eval(self, ctx):
        while self.condition.eval(ctx):
            result = self.body.eval(ctx)
            if isinstance(result, BreakSignal):
                break
            elif isinstance(result, ReturnSignal):
                return result

@dataclass
class Return(Stmt):
    value: Optional[Expr]

    def eval(self, ctx):
        val = self.value.eval(ctx) if self.value else None
        if hasattr(ctx, "expected_return_type") and val is not None:
            if not check_type(ctx.expected_return_type, val):
                raise TypeError(f"Tipo de retorno incorreto: esperado {ctx.expected_return_type}, recebeu {type(val).__name__}")
        return ReturnSignal(val)

@dataclass
class Function(Stmt):
    name: str
    params: List[tuple[str, str]]
    body: Block
    ret_type: str

    def eval(self, ctx):
        ctx[self.name] = self

    def call(self, args, ctx):
        new_ctx = ctx.copy()
        new_ctx.expected_return_type = self.ret_type
        for (tipo, var), arg in zip(self.params, args):
            evaluated_arg = arg.eval(ctx)
            if not check_type(tipo, evaluated_arg):
                raise TypeError(f"Tipo incorreto no argumento '{var.name}': esperado {tipo}, recebeu {type(evaluated_arg).__name__}")
            new_ctx.var_def(var.name, tipo, evaluated_arg)
        result = self.body.eval(new_ctx)
        if isinstance(result, ReturnSignal):
            return result.value
        return result

@dataclass
class FunctionCall(Expr):
    name: str
    args: List[Expr]

    def eval(self, ctx):
        func = ctx.get(self.name)
        if not isinstance(func, Function):
            raise TypeError(f"'{self.name}' não é uma função.")
        return func.call(self.args, ctx)

@dataclass
class Program:
    body: List[Stmt]

    def eval(self, ctx):
        for stmt in self.body:
            result = stmt.eval(ctx)
            if isinstance(result, (BreakSignal, ReturnSignal)):
                return result
        return None

@dataclass
class And(Expr):
    left: Expr
    right: Expr

    def eval(self, ctx):
        return self.left.eval(ctx) and self.right.eval(ctx)

@dataclass
class Or(Expr):
    left: Expr
    right: Expr

    def eval(self, ctx):
        return self.left.eval(ctx) or self.right.eval(ctx)

def add(left, right):
    return left + right

def sub(left, right):
    return left - right

def mul(left, right):
    return left * right

def div(left, right):
    return left / right

def check_type(tipo: str, val) -> bool:
    if tipo == "int":
        return isinstance(val, int)
    elif tipo == "char":
        return isinstance(val, str) and len(val) == 1
    elif tipo == "bool":
        return isinstance(val, bool)
    return False
