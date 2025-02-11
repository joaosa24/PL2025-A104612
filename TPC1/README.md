# TPC1 - Trabalho Prático semana 1 (11/02/2025)

## Informação do Aluno
- **Nome:** João Pedro Ribeiro de Sá
- **Nº:** A104612
- **Foto:**
![Foto](https://avatars.githubusercontent.com/u/116807604?v=4)

## Resumo
Este programa implementa um somador, que opera com base em "interruptores" ON/OFF no input desejado. Este analisa um texto (pode ser alterado pelo utilizador) e soma as sequências de números, quando se encontra com o estado "ON". O programa desenvolvido lida tanto com números positivos como negativos. Se o caracter '=' aparecer, o resultado atual da soma é apresentado. Quando o texto acaba, é apresentado o resultado final.

### Funcionalidades Principais:
- **Sistema ON/OFF**: Reconhecimento de comandos "ON" e "OFF" (lida com todas as variantes, como por exemplo On/ON/oN/on)
- **Processamento Numérico**: Capacidade de processar números positivos e negativos
- **Resultados Parciais**: Mostra resultados sempre que encontra o caractere '='
- **Interface Intuitiva**: Utiliza a biblioteca colorama para apresentação visual dos resultados
- **Processamento de Arquivo de Texto**: Lê dados de um arquivo 'input.txt'

## Componentes do Programa:
1. **Função somadorOnOFF**:
   - Processa o texto caractere por caractere
   - Controla o estado ON/OFF
   - Acumula soma quando apropriado
   - Mostra resultados parciais e finais

2. **Função main**:
   - Interface do usuário com menu
   - Loading do arquivo a ser analisado
   - Controla o fluxo do utilizador

## Dependências e utilização:
1. Biblioteca colorama:
   ```sh
   pip install colorama
   ```
2. Execução
   ```sh
   python3 somadorOnOff.py
   ```
   Para alterar o texto a analisar, deve alterar o arquivo [input.txt](input.txt)

## Lista de Resultados:
- [somadorOnOff.py](somadorOnOff.py)
- [input.txt](input.txt)

## Notas Adicionais:
- Assumo que a flag começa a False, ou seja, é necessário um "On" para começar a soma
- Se ocorrer um "off/on" no meio de uma palavra, esse segmento é considerado para alterar o estado (one altera o estado para on)
