from lark import Lark
from ast_c import *  # Ajuste conforme necessário
from transformer import ASTTransformer
from evaluator import Interpreter
import ast

# Carrega a gramática da linguagem
with open("grammar.lark", "r", encoding="utf-8") as f:
    grammar = f.read()

# Função que parseia o código usando a gramática
def parse(code: str):
    parser = Lark(grammar, parser="lalr", start="program")
    tree = parser.parse(code)  # ← veja se quebra aqui já
    
    transformer = ASTTransformer(interpreter=Interpreter())
    return transformer.transform(tree)

# Função para aplicar indentação ao código
def indent_code(code: str) -> str:
    lines = code.splitlines()
    indented = []
    indent_level = 0
    for line in lines:
        stripped = line.strip()
        if stripped.endswith('{'):
            indented.append('    ' * indent_level + stripped)
            indent_level += 1
        elif stripped.endswith('}'):
            indent_level = max(indent_level - 1, 0)
            indented.append('    ' * indent_level + stripped)
        else:
            indented.append('    ' * indent_level + stripped)
    return '\n'.join(indented)

# Exemplo embutido para comparação
code_literal = """int main(){
    print("Hello, World!");
    return 0;
}
"""

# Solicita o caminho do arquivo .c ao usuário
arquivo = input(
    "Digite o caminho do arquivo .c que deseja interpretar:\n"
    "exemplo: exemplos/fibonacci.c\n"
)

try:
    # Lê o conteúdo do arquivo .c
    with open(arquivo, "r", encoding="utf-8") as code_file:
        raw_code = code_file.read()

    # Aplica indentação ao conteúdo
    code = indent_code(raw_code)

    # Normaliza quebras de linha, BOM invisível e adiciona quebra final
    code = code.replace('\ufeff', '').replace('\r\n', '\n').replace('\r', '\n')
    if not code.endswith('\n'):
        code += '\n'

    # Envolve como string literal e avalia para simular comportamento de code_literal
    code_wrapped = f'"""{code}"""'
    code_clean = ast.literal_eval(code_wrapped)

    # Executa o parser e o interpretador
    ast_tree = parse(code_clean)
    interpreter = Interpreter()
    resultado = interpreter.execute(ast_tree)
except FileNotFoundError:
    print("❌ Arquivo não encontrado. Verifique o caminho e tente novamente.")
except Exception as e:
    print("⚠️ Ocorreu um erro ao processar o arquivo:")
    print(e)
