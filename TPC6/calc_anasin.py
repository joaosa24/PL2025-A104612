from calc_analex import lexer
from calc_ast import Node

def rec_Parser(text):
    lexer.input(text)
    current_token = lexer.token()
    
    def get_token():
        nonlocal current_token
        current_token = lexer.token()
    
    def factor():
        if current_token.type == 'NUM':
            node = Node('num', current_token.value)
            get_token()
            return node
        elif current_token.type == 'LP':
            get_token()
            node = exp()
            if current_token.type == 'RP':
                get_token()
                return node
            raise SyntaxError('Parêntesis não fechado')
        raise SyntaxError('Token inválido')
    
    def term():
        node = factor()
        while current_token and current_token.type in ['TIMES', 'DIV']:
            op = current_token.type.lower()
            get_token()
            node = Node(op, left=node, right=factor())
        return node
    
    def exp():
        node = term()
        while current_token and current_token.type in ['PLUS', 'MINUS']:
            op = current_token.type.lower()
            get_token()
            node = Node(op, left=node, right=term())
        return node
    
    return exp()
