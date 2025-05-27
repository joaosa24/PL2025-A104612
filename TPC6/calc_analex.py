import ply.lex as lex

tokens = ['NUM', 'PLUS', 'MINUS', 'TIMES', 'DIV', 'LP', 'RP']

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIV = r'/'
t_LP = r'\('
t_RP = r'\)'
t_NUM = r'\d+'

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f'Carácter ilegal: {t.value[0]}')
    t.lexer.skip(1)

lexer = lex.lex()
