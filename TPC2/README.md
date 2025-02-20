# TPC2 - Trabalho Prático Semana 2 (11/02/2025)

## Informação do Aluno
- **Nome:** João Pedro Ribeiro de Sá
- **Nº:** A104612
- **Foto:**
![Foto](https://avatars.githubusercontent.com/u/116807604?v=4)

## Resumo
Este programa implementa um script para processar dados de obras musicais. O programa lê informações de um arquivo CSV contendo detalhes sobre obras musicais, incluindo títulos, períodos e compositores. O script organiza e analisa estes dados, gerando três outputs principais: lista de compositores, contagem de obras por período, e títulos organizados por período.

### Funcionalidades Principais:
- **Processamento do CSV**: Capacidade de ler e processar arquivos CSV com campos delimitados por ponto e vírgula (sem a utilização do módulo csv)
- **Gestão dos dados**: Criação de um conjunto único de compositores / Contabilização de obras por período musical / Agrupamento e ordenação de títulos por período
- **Interface Intuitiva**: Utiliza a biblioteca colorama para apresentação visual dos resultados
- **Output dos Dados**: Gera arquivos de texto organizados com os resultados e permite ao utilizador consultar os mesmos no terminal

## Componentes do Programa:
1. **Função parser**:
   - Processa o arquivo CSV
   - Extrai e organiza informações relevantes
   - Gere os conjuntos e dicionários de dados

2. **Função handle_outputs**:
   - Interface do utilizador com opções de visualização
   - Exportação de dados para arquivos
   - Apresentação formatada dos resultados

3. **Função open_csv**
   - Leitura do arquivo CSV

## Dependências e utilização:
1. Biblioteca colorama:
   ```sh
   pip install colorama
   ```
2. Execução
   ```sh
   python3 processadorObras.py
   ```

## Lista de Resultados:
- [Composers.txt](Composers.txt)
- [WorksPerPeriod.txt](WorksPerPeriod.txt)
- [TitlesPerPeriod.txt](TitlesPerPeriod.txt)
- [processadorObras.py](processadorObras.py)
- [obras.csv](obras.csv)

## Notas Adicionais:
- Registros com campos em falta são ignorados