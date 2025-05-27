# TPC5 - Máquina de Vending (14/03/2024)

## Autor
- **Nome:** João Manuel Machado da Cunha
- **Nº:** A104611
![Foto](https://avatars.githubusercontent.com/u/131183584?v=4)

## Descrição do Problema
Desenvolvimento de um simulador de uma máquina de vending que:
- Mantém um stock de produtos (nome, quantidade, preço)
- Aceita moedas (euros e cêntimos)
- Permite selecionar produtos
- Dá troco
- Persiste o estado em ficheiro JSON

## Funcionalidades
- **LISTAR**: Mostra produtos disponíveis
- **MOEDA**: Aceita moedas (1e, 2e, 5c, 10c, 20c, 50c)
- **SELECIONAR**: Permite escolher produtos por código
- **SAIR**: Termina operação e devolve troco

## Exemplo de Utilização

```
maq: 2024-03-14, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> LISTAR
maq:
COD    | NOME           | QUANTIDADE  | PREÇO
-----------------------------------------------
A23    | água 0.5L     | 8          | 70c
B45    | Coca-Cola     | 5          | 120c
C12    | Snack         | 10         | 100c

>> MOEDA 1e, 20c, 5c
maq: Recebi 3 moedas.
maq: Saldo = 1e25c

>> SELECIONAR A23
maq: Pode retirar o produto dispensado "água 0.5L"
maq: Saldo = 55c

>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 5c
maq: Até à próxima
```

## Estrutura do Projeto
- `main.py`: Programa principal
- `VendingMachine.py`: Classe principal da máquina
- `Product.py`: Classe para representação de produtos
- `stock.json`: Ficheiro de persistência do stock

## Como Executar
```bash
python main.py
```

## Notas Técnicas
- Utiliza PLY (Python Lex-Yacc) para análise léxica dos comandos
- Persistência de dados em JSON
- Formatação tabular dos produtos
- Cálculo automático de troco otimizado