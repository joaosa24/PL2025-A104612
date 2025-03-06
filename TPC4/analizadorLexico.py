import re

def tokenize(code):
    token_specification = [
        ('KEYWORD', r'select|where|limit', re.IGNORECASE), # re.IGNORECASE faz com que a regex ignore se a palavra está em maiúscula ou minúscula
        ('VAR', r'\?[a-zA-Z_][a-zA-Z_0-9]*'), # Variáveis começam com ? e podem conter letras, números e underline
        ('URI', r'dbo:[a-zA-Z_][a-zA-Z_0-9]*|foaf:[a-zA-Z_][a-zA-Z_0-9]*'), # URIs começam com dbo: ou foaf: e podem conter letras, números e underline
        ('STRING', r'".*?"(@[a-zA-Z]+)?'), # Strings começam e terminam com aspas duplas e podem conter qualquer caractere, exceto aspas duplas
        ('NUMBER', r'\d+'), # Números são sequências de dígitos
        ('SYMBOL', r'[{}.]'), # Símbolos são {, }, .
        ('WHITESPACE', r'\s+'), # Espaços em branco
        ('UNKNOWN', r'.'), # Qualquer outro caractere
    ]
    
    tok_regex = '|'.join([f'(?P<{id}>{expreg})' for id, expreg, *_ in token_specification]) # Cria uma regex com os padrões definidos
    tokensReconhecidos = [] # Lista que armazenará os tokens reconhecidos
    linhaAtual = 1 # Variável que armazenará a linha atual do código
    
    for mo in re.finditer(tok_regex, code): 
        tipo = mo.lastgroup # Extrai o nome do grupo que deu match
        value = mo.group(tipo) # Extrai o valor que deu match
        
        # Verifica o tipo do token e o adiciona à lista de tokens reconhecidos
        if tipo == 'KEYWORD': 
            tokensReconhecidos.append((value, 'KEYWORD'))
        elif tipo == 'VAR': 
            tokensReconhecidos.append((value, 'VAR'))
        elif tipo == 'URI':
            tokensReconhecidos.append((value, 'URI'))
        elif tipo == 'STRING':
            tokensReconhecidos.append((value, 'STRING'))
        elif tipo == 'NUMBER':
            tokensReconhecidos.append((value, 'NUMBER'))
        elif tipo == 'SYMBOL':
            tokensReconhecidos.append((value, 'SYMBOL'))
        elif tipo == 'WHITESPACE': 
            linhaAtual += value.count('\n')  # Conta o número de linhas
        elif tipo == 'UNKNOWN':
            pass
        
    return tokensReconhecidos

def main():
    with open('query.txt', 'r', encoding='utf-8') as file:  # Abre o arquivo de texto com a query
        query = file.read()  # Lê o conteúdo do arquivo
        
    tokens = tokenize(query)  # Chama a função tokenize para reconhecer os tokens
    
    # Abrir o arquivo output.txt para escrita
    with open('output.txt', 'w', encoding='utf-8') as output_file:
        # Zona de output para o console e arquivo
        output = []
        output.append("Tokens Reconhecidos:") 
        output.append("-" * 30)
        
        for token in tokens:  
            valor, tipo = token
            output.append(f"Valor: {valor.ljust(10)} | Tipo: {tipo}") 
        
        output.append("-" * 30)
        output.append(f"Total de Tokens: {len(tokens)}")
        
        # Escreve no arquivo output.txt
        output_file.write("\n".join(output))
        
        # Exibe na tela o mesmo conteúdo
        for line in output:
            print(line)
        
        print()
        print("OUTPUT FOI GUARDADO EM OUTPUT.TXT")

if __name__ == '__main__':
    main()