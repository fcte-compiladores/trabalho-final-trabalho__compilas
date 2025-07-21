from lark import Transformer, v_args
from ast_c import *
from utils import bin_ops

@v_args(inline=True)
class ASTTransformer(Transformer):
    def __init__(self, interpreter):
        self.functions = {}
        self.interpreter = interpreter

    def program(self, *declarations):
        if 'main' not in self.functions:
            raise ValueError("Função 'main' não encontrada no programa.")
        program = Program(list(declarations))
        program.functions = self.functions
        return program

    def declaration(self, decl):
        return decl

    def var_def(self, type, var, value=None):
        return VarDef(name=var.name, value=value, type=type)

    def function(self, type_tok, name_tok, args, body: Block):
        func = Function(name=name_tok.name, params=args, body=body, ret_type=type_tok)
        self.functions[name_tok.name] = func
        return func

    def call(self, func_name, *args):
        if isinstance(func_name, Var):
            flattened_args = []
            for arg in args:
                if isinstance(arg, list):
                    flattened_args.extend(arg)
                else:
                    flattened_args.append(arg)
            return FunctionCall(name=func_name.name, args=flattened_args)
        raise TypeError("Chamada de função inválida")

    def fun_params(self, *vars):
        params = []
        for i in range(0, len(vars), 2):  
            tipo = vars[i]
            var = vars[i+1]
            if isinstance(var, Var):
                params.append((tipo, var))
            else:
                params.append((tipo, var))
        return params

    def block(self, *declarations):
        return Block(stmts=list(declarations))

    def print_cmd(self, expr):
        return Print(expr=expr)

    def if_cmd(self, cond, then_stmt, else_stmt=None):
        return If(condition=cond, then_branch=then_stmt, else_branch=else_stmt or Block([]))
    
    def break_cmd(self, items=None):
        return Break()

    def while_cmd(self, cond, body):
        return While(condition=cond, body=body)

    def for_cmd(self, args, body):
        init, cond, incr = args
        return Block(stmts=[init, While(cond or Literal(True), body=Block([body, incr]))])

    def for_args(self, arg1=None, cond=None, incr=None):
        return (arg1, cond, incr)


    def opt_expr(self, expr=None):
        return expr or Literal(True)

    def return_cmd(self, expr=None):
        return Return(value=expr or Literal(None))

    def assign(self, var, value):
        return Assign(name=var.name, value=value)

    def params(self, *args):
        return list(args)

    def add(self, left, right): return BinOp(left=left, right=right, op=bin_ops['+'])
    def sub(self, left, right): return BinOp(left=left, right=right, op=bin_ops['-'])
    def mul(self, left, right): return BinOp(left=left, right=right, op=bin_ops['*'])
    def div(self, left, right): return BinOp(left=left, right=right, op=bin_ops['/'])
    def eq(self, left, right): return BinOp(left=left, right=right, op=bin_ops['=='])
    def ne(self, left, right): return BinOp(left=left, right=right, op=bin_ops['!='])
    def gt(self, left, right): return BinOp(left=left, right=right, op=bin_ops['>'])
    def lt(self, left, right): return BinOp(left=left, right=right, op=bin_ops['<'])
    def ge(self, left, right): return BinOp(left=left, right=right, op=bin_ops['>='])
    def le(self, left, right): return BinOp(left=left, right=right, op=bin_ops['<='])
    
    def and_(self, left, right): return And(left=left, right=right)
    def or_(self, left, right): return Or(left=left, right=right)

    def VAR(self, token):
        return Var(token.value)

    def TYPE(self, token):
        return token.value

    def NUMBER(self, token):
        value = float(token) if "." in token or "e" in token.lower() else int(token)
        return Literal(value=value)

    def BOOL(self, token):
        return Literal(value=(token == "true"))

    def STRING(self, token):
        return Literal(value=token[1:-1])

    def VOID(self, token):
        return Literal(value=None)
