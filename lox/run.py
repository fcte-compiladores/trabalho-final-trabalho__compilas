import ast_c
from ctxMinic import ctx
from utils import bin_ops  

def eval_expr(expr, ctx):
    """Avalia uma expressão, retornando seu valor, no ctxo `ctx`."""
    if isinstance(expr, ast_c.Int):
        return expr.value
    elif isinstance(expr, ast_c.Var):
        return ctx.get(expr.name)
    elif isinstance(expr, ast_c.BinaryOp):
        left = eval_expr(expr.left, ctx)
        right = eval_expr(expr.right, ctx)
        return bin_ops[expr.op](left, right)
    else:
        raise Exception(f"Tipo de expressão desconhecido: {expr}")

def exec_stmt(stmt, ctx):
    """Executa um comando no ctxo, e retorna o valor se necessário (como no caso de 'return')."""
    if isinstance(stmt, ast_c.VarDecl):
        value = eval_expr(stmt.expr, ctx)
        ctx.set(stmt.name, value)
    elif isinstance(stmt, ast_c.Return):
        return eval_expr(stmt.expr, ctx)
    elif isinstance(stmt, ast_c.Print):
        print(eval_expr(stmt.expr, ctx))  
    else:
        raise Exception(f"Comando desconhecido: {stmt}")

def run_function(func):
    """Executa uma função, avaliando seu corpo no ctxo."""
    if not isinstance(func, ast_c.Function):
        raise TypeError(f"Esperado um objeto do tipo Function, mas recebeu: {type(func)}")

    print(f"Executando função: {func.name}")
    ctx = ctx()  # Cria um novo ctxo para a execução

    for stmt in func.body:
        print(f"Executando comando: {stmt}")
        result = exec_stmt(stmt, ctx)
        if result is not None:
            return result
    return None
