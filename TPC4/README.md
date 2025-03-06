# TPC4 - Trabalho Prático Semana 6 (06/03/2025)

## Informação do Aluno
- **Nome:** João Pedro Ribeiro de Sá
- **Nº:** A104612
- **Foto:**

![Foto](https://avatars.githubusercontent.com/u/116807604?v=4)

## Resumo
Este programa implementa um **Analisador Léxico** para processar uma linguagem específica. O script identifica e categoriza palavras-chave, variáveis, URIs, strings, números, símbolos e espaços em branco no código, gerando uma lista de tokens reconhecidos.

### Funcionalidades Principais:
- **Identificação de Palavras-chave**: Reconhece palavras-chave como `select`, `where`, `limit` e converte-las para o tipo correspondente.
- **Identificação de Variáveis**: Reconhece variáveis no formato `?nome` e classifica como variáveis.
- **Identificação de URIs**: Processa URIs nos formatos `dbo:uri` e `foaf:uri`.
- **Identificação de Strings**: Converte texto entre aspas duplas para o tipo de token de string.
- **Identificação de Números**: Reconhece números inteiros.
- **Identificação de Símbolos**: Processa símbolos como `{`, `}`, `.`.
- **Contagem de Linhas**: Identifica espaços em branco e conta a quantidade de quebras de linha.
- **Geração de Tokens**: Produz tokens com os tipos e valores correspondentes, exibindo-os na tela e também colocando os mesmos no arquivo `output.txt`.

## Componentes do Programa:
1. **Função tokenize**:
   - Processa o código de entrada e gera uma lista de tokens reconhecidos, categorizando-os de acordo com suas expressões regulares.

2. **Função main**:
   - Lê o conteúdo de um arquivo `query.txt`, chama a função `tokenize` para obter os tokens e os imprime na tela.
   - Também grava a saída no arquivo `output.txt`.

## Utilização:
1. Execução:
   ```sh
   python3 analizadorLexico.py
    ```

## Lista de Resultados:
- [output.txt](output.txt)
- [query.txt](query.txt)
- [analizadorLexico.py](analizadorLexico.py)

## Notas Adicionais
- As expressões regulares são usadas para identificar e classificar os tokens no código.
- O script processa uma query de exemplo e gera um arquivo de saída com os tokens reconhecidos.
- Cada token é impresso no terminal com seu valor e tipo, e a saída também é colocada no arquivo `output.txt`