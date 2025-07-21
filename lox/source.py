from lark import Lark
from ast_c import *  # Ajuste conforme necessário
from transformer import ASTTransformer
from evaluator import Interpreter

with open("grammar.lark") as f:
    grammar = f.read()

# Função que parseia o código
def parse(code: str):
    parser = Lark(grammar, parser="lalr", start="program")
    tree = parser.parse(code)
    transformer = ASTTransformer(interpreter=Interpreter())
    return transformer.transform(tree)

# Ajuste na função fibonacci
arquivo = input("Digite o caminho do arquivo .c que deseja interpretar: \nexemplo: exemplos/fibonacci.c\n")

try:
    with open(arquivo, "r") as code_file:
        code = code_file.read()

    ast = parse(code)
    interpreter = Interpreter()
    resultado = interpreter.execute(ast)
    print("Resultado da execução:", resultado)

except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho e tente novamente.")
except Exception as e:
    print("Ocorreu um erro ao processar o arquivo:", e)
