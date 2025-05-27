# TPC6 - Parser de Expressões Aritméticas (21/03/2024)

## Autor
- **Nome:** João Manuel Machado da Cunha
- **Nº:** A104611

![Foto](https://avatars.githubusercontent.com/u/131183584?v=4)

## Descrição do Problema
Desenvolvimento de um parser LL(1) recursivo descendente que reconhece expressões aritméticas e calcula o seu valor. O parser deve suportar:
- Números inteiros
- Operações básicas (+, -, *, /)
- Parêntesis para definir precedência
- Avaliação da expressão

## Funcionalidades
- Análise léxica dos tokens
- Análise sintática recursiva descendente
- Construção de AST (Abstract Syntax Tree)
- Avaliação das expressões
- Suporte para precedência de operadores
- Tratamento de erros sintáticos

## Exemplo de Utilização
```
calc> 2+3
= 5
calc> 67-(2+3*4)
= 53
calc> (9-2)*(13-4)
= 63
```

## Gramática
```
Exp  -> Term ExpR
ExpR -> + Term ExpR | - Term ExpR | ε
Term -> Fact TermR
TermR -> * Fact TermR | / Fact TermR | ε
Fact -> num | ( Exp )
```

## Estrutura do Projeto
- `calc_program.py`: Programa principal e interface com usuário
- `calc_analex.py`: Analisador léxico usando PLY
- `calc_ast.py`: Classes para representação da AST
- `calc_anasin.py`: Parser recursivo descendente

## Como Executar
```bash
python calc_program.py
```

## Notas Técnicas
- Implementação usando PLY (Python Lex) para análise léxica
- Parser implementado manualmente sem uso de ferramentas de parsing
- AST para representação intermediária e avaliação
- Tratamento de precedência através da estrutura gramatical
