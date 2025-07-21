from ctxMinic import Ctx as Context
from ast_c import Function, Print, VarDef, Block, Return

class Interpreter:
    def __init__(self):
        self.ctx = Context()

    def execute(self, program):
        for func in program.body:
            if isinstance(func, Function):
                self.ctx.set_function(func.name, func)

        if not self.ctx.get("main"):
            raise ValueError("Função 'main' não encontrada.")
        
        print("Executando 'main'...")
        main_func = self.ctx.get("main")
        return main_func.call([], self.ctx)
