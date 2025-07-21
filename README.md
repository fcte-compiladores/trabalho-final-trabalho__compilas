# 🧾 Compilador para Mini-C

## 👥 Integrantes

- Nome: Arthur Guilherme Aquino Santos  
  Matrícula: 231037656  
  Turma: T02 (2025.1-46T45)

- Nome: João Igor Pereira da Costa  
  Matrícula: 231027201  
  Turma: T02 (2025.1-46T45)

- Nome: Tiago Lemes Teixeira  
  Matrícula: 231026581  
  Turma: T02 (2025.1-46T45)

- Nome: Yzabella Miranda Pimenta  
  Matrícula: 231039187  
  Turma: T02 (2025.1-46T45)

---

## 🧠 Introdução

Este projeto desenvolve um **interpretador** para uma linguagem baseada em um subconjunto simplificado da linguagem C, denominada **Mini-C**. O objetivo é permitir a execução de programas com estruturas típicas de C, como expressões aritméticas, controle de fluxo, definição de funções e impressão de valores.

### Funcionalidades implementadas:

- Declaração e atribuição de variáveis com tipos (`int`, `char`, `bool`)
- Expressões aritméticas e booleanas
- Comandos de controle: `if`, `else`, `while`, `break`, `return`
- Funções com parâmetros e retorno
- Impressão de valores (`printf`)
- Escopos com blocos `{}` e ambiente de execução aninhado

### Estratégias utilizadas:

- **Análise léxica e sintática** com Lark, usando uma gramática LALR (`grammar.lark`)
- **Transformação da árvore sintática (parse tree) em AST**, com a classe `ASTTransformer`
- **Execução da AST** com um interpretador baseado em visitas (`evaluator.py`)
- Contexto de execução controlado por escopos (`ctxMinic.py`)

---

## ⚙️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/fcte-compiladores/trabalho-final-trabalho__compilas.git
cd seu-repositorio
```

2. (Opcional) Instale o gerenciador de pacotes uv, caso ainda não tenha:
```bash
uv pip install uv
```

3. Instale as dependências:
```bash
uv pip install -r requirements.txt
```

---


## 📚 Referências

As principais referências utilizadas para a realização do trabalho foram: 

- [Repositório da disciplina Compiladores 1 (FCTE, 2025/1)](https://github.com/fcte-compiladores/2025-1)  
  Serviu como base inicial para a estrutura do projeto e forneceu exemplos de interpretadores em Python, incluindo o Lox, usados como inspiração para a arquitetura geral do compilador.

- [Crafting Interpreters, Robert Nystrom, 2015–2021](https://craftinginterpreters.com/)  
  Livro fundamental para o desenvolvimento do interpretador, guiando a construção de analisadores léxicos e sintáticos, ASTs e o padrão de visitantes, adaptados para a linguagem Mini-C.

- [Documentação oficial da linguagem C (ISO C)](https://en.cppreference.com/w/c)  
  Utilizada como base para definir a sintaxe, tipos primitivos e semântica da linguagem Mini-C, garantindo maior fidelidade à linguagem C original.

---

## 🧩 Estrutura do Código

- `ast_c.py`: definição da AST (expressões, comandos, funções, blocos, etc.)
- `ctxMinic.py`: implementação do contexto de execução (escopos, variáveis, funções)
- `evaluator.py`: interpretador que executa a AST
- `grammar.lark`: gramática LALR da linguagem Mini-C
- `source.py`: ponto de entrada, faz parsing e chama o interpretador
- `errors.py`: erros semânticos personalizados
- `run.py`: utilitário auxiliar com funções alternativas de execução

Etapas da compilação:

- **Léxica/Sintática**: `Lark` com gramática definida
- **AST**: transformação com `ASTTransformer`
- **Execução**: AST interpretada por `Interpreter` com `Ctx`

---

## 🐞 Bugs / Limitações

- Não há suporte a vetores ou structs
- Tipagem é estática, mas limitada (sem coerção automática entre tipos)
- Ainda não há suporte a `for`
- Não há suporte a escopos globais separados de funções
- Erros de execução ainda são genéricos em alguns pontos

### Melhorias possíveis

- Implementar suporte a arrays
- Adicionar operadores lógicos completos (`!=`, `<=`, etc.)
- Suporte a `for`, `continue`, `do while`
- Melhoria nas mensagens de erro e validações
- Suporte a tipos compostos (ex: structs)

---