import sys
import ply.lex as lex

# Estados para strings e comentários
states = (
    ('string', 'exclusive'),
    ('comment', 'exclusive'),
)

tokens = (
    'ID', 'NUMBER', 'STRING', 'CHAR',
    # Operadores
    'ADD', 'SUB', 'MUL', 'DIVIDE', 'MOD',
    'ASSIGN', 'EQUAL', 'NOTEQUAL', 'SMALLERTHEN', 'BIGGERTHEN', 'SMALOREQ', 'BIGOREQ',
    # Delimitadores
    'SEMICOLON', 'COLON', 'COMMA', 'DOT', 'DOTDOT',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    # Palavras reservadas
    'AND', 'ARRAY', 'BEGIN', 'BOOLEAN', 'CASE', 'CONST', 'CHAR_TYPE',
    'DIV', 'DO', 'DOWNTO', 'ELSE', 'END', 'FALSE',
    'FOR', 'FUNCTION', 'IF', 'INTEGER', 'NOT', 'OF',
    'OR', 'PROCEDURE', 'PROGRAM', 'READ', 'READLN',
    'REAL', 'REPEAT', 'STRING_TYPE', 'THEN', 'TO',
    'TRUE', 'UNTIL', 'VAR', 'WHILE', 'WRITE', 'WRITELN'
)

# Operadores e delimitadores
t_ASSIGN = r':='
t_DOTDOT = r'\.\.'
t_SMALOREQ = r'<='
t_BIGOREQ = r'>='
t_NOTEQUAL = r'<>'
t_EQUAL = r'='
t_SMALLERTHEN = r'<'
t_BIGGERTHEN = r'>'
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIVIDE = r'/'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

def t_AND(t):
    r'(?i)\band\b'
    return t

def t_ARRAY(t):
    r'(?i)\barray\b'
    return t

def t_BEGIN(t):
    r'(?i)\bbegin\b'
    return t

def t_BOOLEAN(t):
    r'(?i)\bboolean\b'
    return t

def t_CASE(t):
    r'(?i)\bcase\b'
    return t

def t_CONST(t):
    r'(?i)\bconst\b'
    return t

def t_DIV(t):
    r'(?i)\bdiv\b'
    return t

def t_DOWNTO(t):
    r'(?i)\bdownto\b'
    return t

def t_DO(t):
    r'(?i)\bdo\b'
    return t

def t_ELSE(t):
    r'(?i)\belse\b'
    return t

def t_END(t):
    r'(?i)\bend\b'
    return t

def t_FALSE(t):
    r'(?i)\bfalse\b'
    return t

def t_FOR(t):
    r'(?i)\bfor\b'
    return t

def t_FUNCTION(t):
    r'(?i)\bfunction\b'
    return t

def t_IF(t):
    r'(?i)\bif\b'
    return t

def t_INTEGER(t):
    r'(?i)\binteger\b'
    return t

def t_MOD(t):
    r'(?i)\bmod\b'
    return t

def t_NOT(t):
    r'(?i)\bnot\b'
    return t

def t_OF(t):
    r'(?i)\bof\b'
    return t

def t_OR(t):
    r'(?i)\bor\b'
    return t

def t_PROCEDURE(t):
    r'(?i)\bprocedure\b'
    return t

def t_PROGRAM(t):
    r'(?i)\bprogram\b'
    return t

def t_READLN(t):
    r'(?i)\breadln\b'
    return t

def t_READ(t):
    r'(?i)\bread\b'
    return t

def t_REAL(t):
    r'(?i)\breal\b'
    return t

def t_REPEAT(t):
    r'(?i)\brepeat\b'
    return t

def t_STRING_TYPE(t):
    r'(?i)\bstring\b'
    return t

def t_CHAR_TYPE(t):
    r'(?i)\bchar\b'
    return t

def t_THEN(t):
    r'(?i)\bthen\b'
    return t

def t_TO(t):
    r'(?i)\bto\b'
    return t

def t_TRUE(t):
    r'(?i)\btrue\b'
    return t

def t_UNTIL(t):
    r'(?i)\buntil\b'
    return t

def t_VAR(t):
    r'(?i)\bvar\b'
    return t

def t_WHILE(t):
    r'(?i)\bwhile\b'
    return t

def t_WRITELN(t):
    r'(?i)\bwriteln\b'
    return t

def t_WRITE(t):
    r'(?i)\bwrite\b'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_CHAR(t):
    r"'([^']|'')'"
    # Remove as aspas e processa escape de aspas duplas
    content = t.value[1:-1]
    if content == "''":
        t.value = "'"
    else:
        t.value = content
    return t

# Strings
def t_begin_string(t):
    r'\''
    t.lexer.string_value = ""
    t.lexer.begin('string')

def t_string_quote(t):
    r'\'\''
    t.lexer.string_value += "'"

def t_string_content(t):
    r'[^\']+'
    t.lexer.string_value += t.value

def t_string_end(t):
    r'\''
    t.type = 'STRING'
    t.value = t.lexer.string_value
    t.lexer.begin('INITIAL')
    return t

# Comentários
def t_begin_comment_brace(t):
    r'\{'
    t.lexer.begin('comment')

def t_begin_comment_paren(t):
    r'\(\*'
    t.lexer.begin('comment')

def t_comment_end_brace(t):
    r'\}'
    t.lexer.begin('INITIAL')

def t_comment_end_paren(t):
    r'\*\)'
    t.lexer.begin('INITIAL')

def t_comment_content(t):
    r'[^}*\n]+'
    pass

def t_comment_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Whitespace e newlines
t_ignore = ' \t'
t_string_ignore = ''
t_comment_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

def t_string_error(t):
    print(f"Illegal string character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

def t_comment_error(t):
    print(f"Illegal comment character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

# Função para teste
def test_lexer(data):
    lexer.input(data)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append((tok.type, tok.value))
    return tokens_list

# Exemplo de uso
if __name__ == "__main__":
    
    with open(sys.argv[1], "r") as file:
        data = file.read()
        
    tokens = test_lexer(data)
    for token in tokens:
        print(token)