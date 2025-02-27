# TPC2 - Trabalho Prático Semana 3 (25/02/2025)

## Informação do Aluno
- **Nome:** João Pedro Ribeiro de Sá
- **Nº:** A104612
- **Foto:**

![Foto](https://avatars.githubusercontent.com/u/116807604?v=4)

## Resumo
Este programa implementa um **conversor de MarkDown para HTML**. O script processa texto em formato *Markdown* e converte-o para os elementos HTML correspondentes. O programa suporta a conversão de várias formatações como cabeçalhos, texto em itálico, negrito, links, imagens e listas numeradas.

### Funcionalidades Principais:
- **Conversão de Cabeçalhos**: Transforma cabeçalhos Markdown (# Título) em tags HTML (`<h1>Titulo</h1>`)
- **Formatação de Texto**: Converte texto em itálico (texto) e negrito (texto) para as respectivas tags HTML
- **Links e Imagens**: Processa links e imagens em formato Markdown para tags *anchor* e *image* em HTML
- **Listas Numeradas**: Converte listas numeradas para o formato ordenado HTML (`<ol>` e `<li>`)
- **Output**: Gera um arquivo (`output.txt`) com os resultados obtidos.

## Componentes do Programa:
1. **Função converterHeader**:
   - Identifica cabeçalhos Markdown
   - Converte para tags HTML `<h1>` a `<h6>` conforme o nível do cabeçalho

2. **Função converterItalico**:
   - Processa texto entre asteriscos simples
   - Gera tags `<i>` correspondentes

3. **Função converterBold**:
   - Processa texto entre asteriscos duplos
   - Gera tags `<b>` correspondentes

4. **Função converterLink**
   - Processa links
   - Transforma em tags *anchor* HTML `<a href="URL">texto</a>`

5. **Função converterImagem**
   - Processa imagens no formato Markdown `![imagem](imagem.png)`
   - Converte para tags `<img>` com atributos *src* e *alt*

6. **Função converterListaOrdenada**:
   - Identifica listas numeradas
   - Transforma em estrutura HTML com tags `<ol>` e `<li>`

## Utilização:
1. Execução
   ```sh
   python3 converterMarkdown.py
   ```

## Lista de Resultados:
- [output.txt](output.txt)
- [converterMarkdown.py](converterMarkdown.py)

## Notas Adicionais:
- As funções utilizam expressões regulares para identificar e processar os padrões Markdown
- Cada função é especializada num tipo específico de conversão
- O programa demonstra o funcionamento com exemplos *hardcoded*
- Os resultados são exibidos de forma organizada no arquivo `output.txt`