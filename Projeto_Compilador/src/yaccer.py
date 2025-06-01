import ply.yacc as yacc
import sys
from anasem import SemanticAnalyzer
from lexer import tokens, lexer

def generate_expr_code(expr):
    """Gera código para uma expressão, fazendo lookup"""
    if isinstance(expr, tuple) and len(expr) == 2 and isinstance(expr[0], str) and expr[0] in parser.symbol_table:
        var_name = expr[0]
        index_expr = expr[1]
        
        if var_name in parser.symbol_table:
            var_info = parser.symbol_table[var_name]
            var_type = var_info['type']
            
            # Array
            if isinstance(var_type, tuple) and var_type[0] == 'array':
                code = "pushgp\n"
                code += f"pushi {var_info['address']}\n"
                code += "padd\n"
                code += generate_expr_code(index_expr)
                
                if var_type[1] != 0:
                    code += f"pushi {var_type[1]}\n"
                    code += "sub\n"
                
                code += "loadn\n"
                return code
            
            # Acesso a caracteres de uma string
            elif var_type == 'string':
                code = f"pushg {var_info['address']}\n"
                code += generate_expr_code(index_expr)
                code += "pushi 1\n"
                code += "sub\n"
                code += "charat\n"
                return code
    
    elif isinstance(expr, tuple) and len(expr) == 2 and isinstance(expr[1], str):
        expr_type, code = expr
        if expr_type in ['integer', 'real', 'boolean', 'char']:
            return code
        elif expr_type == 'string':
            return f"pushs \"{code}\"\n"
    
    # String literal
    elif isinstance(expr, tuple) and len(expr) == 2 and expr[0] == 'string':
        return f"pushs \"{expr[1]}\"\n"
    
    # Variável simples
    elif isinstance(expr, str) and expr in parser.symbol_table:
        return f"pushg {parser.symbol_table[expr]['address']}\n"
    
    # Código já gerado
    elif isinstance(expr, str) and expr not in parser.symbol_table:
        return expr
    
    else:
        return str(expr)

def get_expr_type(expr):
    """Obtém o tipo de uma expressão"""
    if isinstance(expr, tuple) and len(expr) == 2 and isinstance(expr[0], str) and expr[0] in parser.symbol_table:
        var_name = expr[0]
        var_type = parser.symbol_table[var_name]['type']
        if isinstance(var_type, tuple) and var_type[0] == 'array':
            return var_type[3]
        elif var_type == 'string':
            return 'char'
    
    elif isinstance(expr, tuple) and len(expr) == 2 and isinstance(expr[1], str):
        expr_type, _ = expr
        return expr_type
    
    # String literal direta
    elif isinstance(expr, tuple) and len(expr) == 2 and expr[0] == 'string':
        return 'string'
    
    # Variável simples
    elif isinstance(expr, str) and expr in parser.symbol_table:
        var_type = parser.symbol_table[expr]['type']
        return var_type

    return 'integer'

def new_label(parser):
    parser.label_counter += 1
    return f"L{parser.label_counter}"

def p_programa(p):
    'Programa : PROGRAM ID SEMICOLON Bloco DOT'
    code = ""
    if parser.var_counter > 0:
        code = f"pushn {parser.var_counter}\n"
    else:
        code = ""
    code += "start\n"
    code += p[4]
    code += "stop"
    p[0] = code

def p_bloco(p):
    'Bloco : VarSec Exec'
    p[0] = p[2]

def p_varsec1(p):
    'VarSec : VAR ListaDeclaracaoVars'
    p[0] = p[2]

def p_varsec2(p):
    'VarSec : empty'
    p[0] = 0

def p_listadeclaracaovars1(p):
    'ListaDeclaracaoVars : DeclVar ListaDeclaracaoVars'
    p[0] = p[1] + p[2]

def p_listadeclaracaovars2(p):
    'ListaDeclaracaoVars : empty'
    p[0] = 0

def p_declvar(p):
    'DeclVar : ListaVariaveis COLON Tipo SEMICOLON'
    var_count = 0
    tipo = p[3]

    for var_info in p[1]:
        if isinstance(tipo, tuple) and tipo[0] == 'array':
            var_size = tipo[2] - tipo[1] + 1
            var_name = var_info
            
            parser.symbol_table[var_name] = {
                'address': parser.var_counter,
                'type': tipo,
            }
            parser.var_counter += var_size               
            var_count += var_size
        else:
            var_name = var_info
            var_size = 1
            
            parser.symbol_table[var_name] = {
                'address': parser.var_counter,
                'type': tipo
            }
            parser.var_counter += var_size
            var_count += var_size
            
    parser.semantic_analyzer.set_symbol_table(parser.symbol_table)
    p[0] = var_count

def p_variavel1(p):
    'Variavel : ID LBRACKET Expr RBRACKET'
    p[0] = (p[1], p[3])

def p_variavel2(p):
    'Variavel : ID'
    p[0] = p[1]

def p_listavariaveis(p):
    'ListaVariaveis : Variavel ListaVariaveisTail'
    p[0] = [p[1]] + p[2]

def p_listavariaveistail1(p):
    'ListaVariaveisTail : COMMA Variavel ListaVariaveisTail'
    p[0] = [p[2]] + p[3]

def p_listavariaveistail2(p):
    'ListaVariaveisTail : empty'
    p[0] = []

def p_tipo1(p):
    'Tipo : INTEGER'
    p[0] = 'integer'

def p_tipo2(p):
    'Tipo : REAL'
    p[0] = 'real'

def p_tipo3(p):
    'Tipo : CHAR_TYPE'
    p[0] = 'char'

def p_tipo4(p):
    'Tipo : BOOLEAN'
    p[0] = 'boolean'

def p_tipo5(p):
    'Tipo : STRING_TYPE'
    p[0] = 'string'

def p_tipo6(p):
    'Tipo : ARRAY LBRACKET NUMBER DOTDOT NUMBER RBRACKET OF Tipo'
    p[0] = ('array', p[3], p[5], p[8])

def p_exec(p):
    'Exec : BEGIN ListaInstrucao END'
    p[0] = p[2]

def p_listainstrucao1(p):
    'ListaInstrucao : Instrucao SEMICOLON ListaInstrucao'
    p[0] = p[1] + p[3]

def p_listainstrucao2(p):
    'ListaInstrucao : Instrucao'
    p[0] = p[1]

def p_listainstrucao3(p):
    'ListaInstrucao : empty'
    p[0] = ""

def p_instrucao1(p):
    'Instrucao : IF Expr THEN Instrucao'
    if not parser.semantic_analyzer.check_condition_type(get_expr_type(p[2]), 'If statement', p.lineno(1)):
        parser.success = False
        p[0] = ""
        return
    else_label = new_label(parser)
    code = generate_expr_code(p[2])
    code += f"jz {else_label}\n"
    code += p[4]
    code += f"{else_label}:\n"
    p[0] = code

def p_instrucao2(p):
    'Instrucao : IF Expr THEN Instrucao ELSE Instrucao'
    if not parser.semantic_analyzer.check_condition_type(get_expr_type(p[2]), 'If statement', p.lineno(1)):
        parser.success = False
        p[0] = ""
        return
    else_label = new_label(parser)
    end_label = new_label(parser)
    code = generate_expr_code(p[2])
    code += f"jz {else_label}\n"
    code += p[4]
    code += f"jump {end_label}\n"
    code += f"{else_label}:\n"
    code += p[6]
    code += f"{end_label}:\n"
    p[0] = code

def p_instrucao3(p):
    'Instrucao : Loop'
    p[0] = p[1]

def p_instrucao4(p):
    'Instrucao : Atr'
    p[0] = p[1]

def p_instrucao5(p):
    'Instrucao : Exec'
    p[0] = p[1]

def p_instrucao6(p):
    'Instrucao : WRITE LPAREN ListaExpr RPAREN'
    code = ""
    for expr_info in p[3]:
        if isinstance(expr_info, tuple) and expr_info[0] == 'string':
            code += f"pushs \"{expr_info[1]}\"\n"
            code += "writes\n"
        else:
            code += generate_expr_code(expr_info)
            
            expr_type = get_expr_type(expr_info)
            
            if expr_type == 'integer':
                code += "writei\n"
            elif expr_type == 'real':
                code += "writef\n"
            elif expr_type == 'char':
                code += "writechr\n"
            elif expr_type == 'boolean':
                code += "writei\n" 
            elif expr_type == 'string':
                code += "writes\n"
            else:
                code += "writei\n" 
    p[0] = code

def p_instrucao7(p):
    'Instrucao : WRITELN LPAREN ListaExpr RPAREN'
    code = ""
    for expr_info in p[3]:
        if isinstance(expr_info, tuple) and expr_info[0] == 'string':
            code += f"pushs \"{expr_info[1]}\"\n"
            code += "writes\n"
        else:
            code += generate_expr_code(expr_info)
            
            expr_type = get_expr_type(expr_info)
            
            if expr_type == 'integer':
                code += "writei\n"
            elif expr_type == 'real':
                code += "writef\n"
            elif expr_type == 'char':
                code += "writechr\n"
            elif expr_type == 'boolean':
                code += "writei\n"
            elif expr_type == 'string':
                code += "writes\n"
            else:
                code += "writei\n"
    
    code += "writeln\n"
    p[0] = code
    
def p_instrucao8(p):
    'Instrucao : WRITELN'
    code = "writeln\n"
    p[0] = code

def p_instrucao9(p):
    'Instrucao : READ LPAREN ListaVariaveis RPAREN'
    code = ""
    for var_info in p[3]:
        if isinstance(var_info, tuple):
            var_name = var_info[0]
            if var_name in parser.symbol_table:
                mark_variable_used(var_name)
                var_type = parser.symbol_table[var_name]['type']
                
                # Para arrays
                if isinstance(var_type, tuple) and var_type[0] == 'array':
                    code += "pushgp\n"
                    code += f"pushi {parser.symbol_table[var_name]['address']}\n"
                    code += "padd\n"
                    code += generate_expr_code(var_info[1])  # índice
                    
                    lower_bound = var_type[1]  # limite inferior do array
                    if lower_bound != 0:
                        code += f"pushi {lower_bound}\n"
                        code += "sub\n"
                    
                    code += "read\n"
                    code += "atoi\n"
                    code += "storen\n"
                else:
                    code += "read\n"
                    code += "atoi\n"
                    code += f"storeg {parser.symbol_table[var_name]['address']}\n"
            else:
                if not parser.semantic_analyzer.check_variable_declaration(var_name, p.lineno(1)):
                    parser.success = False
                    p[0] = ""
                    return
                    
        elif var_info in parser.symbol_table:
            mark_variable_used(var_info)
            var_type = parser.symbol_table[var_info]['type']
            
            if var_type == 'string':
                code += "read\n"
                code += f"storeg {parser.symbol_table[var_info]['address']}\n"
            else:
                code += "read\n"
                code += "atoi\n"
                code += f"storeg {parser.symbol_table[var_info]['address']}\n"
        else:
            if not parser.semantic_analyzer.check_variable_declaration(var_info, p.lineno(1)):
                parser.success = False
                p[0] = ""
                return
    p[0] = code

def p_instrucao10(p):
    'Instrucao : READLN LPAREN ListaVariaveis RPAREN'
    code = ""
    for var_info in p[3]:
        if isinstance(var_info, tuple):
            var_name = var_info[0]
            if var_name in parser.symbol_table:
                mark_variable_used(var_name)
                var_type = parser.symbol_table[var_name]['type']
                
                # Para arrays
                if isinstance(var_type, tuple) and var_type[0] == 'array':
                    code += "pushgp\n"
                    code += f"pushi {parser.symbol_table[var_name]['address']}\n"
                    code += "padd\n"
                    code += generate_expr_code(var_info[1])  # índice
                    
                    lower_bound = var_type[1]
                    if lower_bound != 0:
                        code += f"pushi {lower_bound}\n"
                        code += "sub\n"
                    
                    code += "read\n"
                    code += "atoi\n"
                    code += "storen\n"
                else:
                    code += "read\n"
                    code += "atoi\n"
                    code += f"storeg {parser.symbol_table[var_name]['address']}\n"
            else:
                if not parser.semantic_analyzer.check_variable_declaration(var_name, p.lineno(1)):
                    parser.success = False
                    p[0] = ""
                    return
                    
        elif var_info in parser.symbol_table:
            mark_variable_used(var_info)
            var_type = parser.symbol_table[var_info]['type']
            
            if var_type == 'string':
                code += "read\n"
                code += f"storeg {parser.symbol_table[var_info]['address']}\n"
            else:
                code += "read\n"
                code += "atoi\n"
                code += f"storeg {parser.symbol_table[var_info]['address']}\n"
        else:
            if not parser.semantic_analyzer.check_variable_declaration(var_info, p.lineno(1)):
                parser.success = False
                p[0] = ""
                return
    p[0] = code

def p_loop1(p):
    'Loop : WHILE Expr DO Instrucao'
    if not parser.semantic_analyzer.check_condition_type(get_expr_type(p[2]), 'While loop', p.lineno(1)):
        parser.success = False
        p[0] = ""
        return
    
    start_label = new_label(parser)
    end_label = new_label(parser)
    code = f"{start_label}:\n"
    code += generate_expr_code(p[2])  # condição
    code += f"jz {end_label}\n"
    code += p[4]  # corpo
    code += f"jump {start_label}\n"
    code += f"{end_label}:\n"
    p[0] = code

def p_loop2(p):
    'Loop : FOR ID ASSIGN Expr TO Expr DO Instrucao'
    if not parser.semantic_analyzer.check_for_loop_bounds(get_expr_type(p[2]), get_expr_type(p[6]), p.lineno(1)):
        parser.success = False
        p[0] = ""
        return
        
    start_label = new_label(parser)
    end_label = new_label(parser)
    
    var_name = p[2]
    if not parser.semantic_analyzer.check_variable_declaration(var_name, p.lineno(1)):
        parser.success = False
        p[0] = ""
        return
    
    mark_variable_used(var_name)
    
    code = generate_expr_code(p[4])
    code += f"storeg {parser.symbol_table[var_name]['address']}\n"
    
    code += f"{start_label}:\n"
    
    code += generate_expr_code(p[6])
    code += f"pushg {parser.symbol_table[var_name]['address']}\n"
    code += "supeq\n"
    code += f"jz {end_label}\n"
    
    code += p[8]
    
    code += f"pushg {parser.symbol_table[var_name]['address']}\n"
    code += "pushi 1\n"
    code += "add\n"
    code += f"storeg {parser.symbol_table[var_name]['address']}\n"
    
    code += f"jump {start_label}\n"
    
    code += f"{end_label}:\n"
    
    p[0] = code
    
def p_loop3(p):
    'Loop : FOR ID ASSIGN Expr DOWNTO Expr DO Instrucao'
    if not parser.semantic_analyzer.check_for_loop_bounds(get_expr_type(p[2]), get_expr_type(p[6]), p.lineno(1)):
        parser.success = False
        p[0] = ""
        return
        
    start_label = new_label(parser)
    end_label = new_label(parser)

    var_name = p[2]
    if not parser.semantic_analyzer.check_variable_declaration(var_name, p.lineno(1)):
        parser.success = False
        p[0] = ""
        return
    
    mark_variable_used(var_name)
    
    code = generate_expr_code(p[4])
    code += f"storeg {parser.symbol_table[var_name]['address']}\n"
    
    code += f"{start_label}:\n"
    
    code += generate_expr_code(p[6])
    code += f"pushg {parser.symbol_table[var_name]['address']}\n"
    code += "infeq\n"
    code += f"jz {end_label}\n"
    
    code += p[8]
    
    code += f"pushg {parser.symbol_table[var_name]['address']}\n"
    code += "pushi 1\n"
    code += "sub\n"
    code += f"storeg {parser.symbol_table[var_name]['address']}\n"
    
    code += f"jump {start_label}\n"
    
    code += f"{end_label}:\n"
    
    p[0] = code

def p_atr1(p):
    'Atr : ID ASSIGN Expr'
    var_name = p[1]
    if var_name in parser.symbol_table:
        mark_variable_used(var_name)
        if not parser.semantic_analyzer.check_assignment_compatibility(var_name, get_expr_type(p[3]), p.lineno(1)):
            parser.success = False
            p[0] = ""
            return
            
        code = generate_expr_code(p[3])  # expressão
        code += f"storeg {parser.symbol_table[var_name]['address']}\n"
        
        if isinstance(p[3], tuple) and len(p[3]) == 2 and p[3][0] == 'string':
            parser.symbol_table[var_name]['value'] = p[3][1]
            
        p[0] = code
    else:
        if not parser.semantic_analyzer.check_variable_declaration(var_name, p.lineno(1)):
            parser.success = False
            p[0] = ""
            return

def p_atr2(p):
    'Atr : ID LBRACKET Expr RBRACKET ASSIGN Expr'
    var_name = p[1]
    if var_name in parser.symbol_table:
        mark_variable_used(var_name)
        var_info = parser.symbol_table[var_name]
        if not parser.semantic_analyzer.check_assignment_compatibility(var_name, get_expr_type(p[6]), p.lineno(1)):
            parser.success = False
            p[0] = ""
            return
            
        if isinstance(var_info['type'], tuple) and var_info['type'][0] == 'array':
            code = "pushgp\n"
            code += f"pushi {var_info['address']}\n"
            code += "padd\n"
            code += generate_expr_code(p[3])  # expressão do índice
            
            if var_info['type'][1] != 0:
                code += f"pushi {var_info['type'][1]}\n"
                code += "sub\n"
            
            code += generate_expr_code(p[6])
            code += "storen\n"
        else:
            code = generate_expr_code(p[6])
            code += f"storeg {parser.symbol_table[var_name]['address']}\n"
        
        p[0] = code
    else:
        if not parser.semantic_analyzer.check_variable_declaration(var_name, p.lineno(1)):
            parser.success = False
            p[0] = ""
            return

def p_expr1(p):
    'Expr : Expr OR TermoAnd'
    if not parser.semantic_analyzer.check_logical_operation(get_expr_type(p[1]), get_expr_type(p[3]), 'OR', p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "or\n"
    p[0] = ('boolean', code)

def p_expr2(p):
    'Expr : TermoAnd'
    p[0] = p[1]
    
def p_listaexpr1(p):
    'ListaExpr : Expr ListaExprTail'
    p[0] = [p[1]] + p[2]

def p_listaexpr2(p):
    'ListaExprTail : COMMA Expr ListaExprTail'
    p[0] = [p[2]] + p[3]

def p_listaexpr3(p):
    'ListaExprTail : empty'
    p[0] = []

def p_termoand1(p):
    'TermoAnd : TermoAnd AND TermoIgualdade'
    if not parser.semantic_analyzer.check_logical_operation(get_expr_type(p[1]), get_expr_type(p[3]), 'AND', p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "and\n"
    p[0] = ('boolean', code)

def p_termoand2(p):
    'TermoAnd : TermoIgualdade'
    p[0] = p[1]

def p_termoigualdade1(p):
    'TermoIgualdade : TermoIgualdade EQUAL TermoRelacional'
    if not parser.semantic_analyzer.check_comparison_operation(get_expr_type(p[1]), get_expr_type(p[3]), "=", p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "equal\n"
    p[0] = ('boolean', code)

def p_termoigualdade2(p):
    'TermoIgualdade : TermoIgualdade NOTEQUAL TermoRelacional'
    if not parser.semantic_analyzer.check_comparison_operation(get_expr_type(p[1]), get_expr_type(p[3]), "<>", p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "equal\nnot\n"
    p[0] = ('boolean', code)

def p_termoigualdade3(p):
    'TermoIgualdade : TermoRelacional'
    p[0] = p[1]

def p_termorelacional1(p):
    'TermoRelacional : TermoRelacional BIGGERTHEN TermoAditivo'
    if not parser.semantic_analyzer.check_comparison_operation(get_expr_type(p[1]), get_expr_type(p[3]), ">", p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "sup\n"
    p[0] = ('boolean', code)

def p_termorelacional2(p):
    'TermoRelacional : TermoRelacional SMALLERTHEN TermoAditivo'
    if not parser.semantic_analyzer.check_comparison_operation(get_expr_type(p[1]), get_expr_type(p[3]), "<", p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "inf\n"
    p[0] = ('boolean', code)

def p_termorelacional3(p):
    'TermoRelacional : TermoRelacional BIGOREQ TermoAditivo'
    if not parser.semantic_analyzer.check_comparison_operation(get_expr_type(p[1]), get_expr_type(p[3]), ">=", p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "supeq\n"
    p[0] = ('boolean', code)

def p_termorelacional4(p):
    'TermoRelacional : TermoRelacional SMALOREQ TermoAditivo'
    if not parser.semantic_analyzer.check_comparison_operation(get_expr_type(p[1]), get_expr_type(p[3]), "<=", p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "infeq\n"
    p[0] = ('boolean', code)

def p_termorelacional5(p):
    'TermoRelacional : TermoAditivo'
    p[0] = p[1]

def p_termoaditivo1(p):
    'TermoAditivo : TermoAditivo ADD TermoMultiplicativo'
    type1 = get_expr_type(p[1])
    type2 = get_expr_type(p[3])
    
    if not parser.semantic_analyzer.check_arithmetic_operation(type1, type2, '+', p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "add\n"
    
    result_type = 'real' if (type1 == 'real' or type2 == 'real') else 'integer'
    p[0] = (result_type, code)

def p_termoaditivo2(p):
    'TermoAditivo : TermoAditivo SUB TermoMultiplicativo'
    type1 = get_expr_type(p[1])
    type2 = get_expr_type(p[3])
    
    if not parser.semantic_analyzer.check_arithmetic_operation(type1, type2, '-', p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "sub\n"
    
    result_type = 'real' if (type1 == 'real' or type2 == 'real') else 'integer'
    p[0] = (result_type, code)

def p_termoaditivo3(p):
    'TermoAditivo : TermoMultiplicativo'
    p[0] = p[1]

def p_termomultiplicativo1(p):
    'TermoMultiplicativo : TermoMultiplicativo MUL Fator'
    type1 = get_expr_type(p[1])
    type2 = get_expr_type(p[3])
    
    if not parser.semantic_analyzer.check_arithmetic_operation(type1, type2, '*', p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "mul\n"
    
    result_type = 'real' if (type1 == 'real' or type2 == 'real') else 'integer'
    p[0] = (result_type, code)

def p_termomultiplicativo2(p):
    'TermoMultiplicativo : TermoMultiplicativo DIV Fator'
    type1 = get_expr_type(p[1])
    type2 = get_expr_type(p[3])
    
    if not parser.semantic_analyzer.check_arithmetic_operation(type1, type2, '/', p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "div\n"
    
    result_type = 'real' if (type1 == 'real' or type2 == 'real') else 'integer'
    p[0] = (result_type, code)

def p_termomultiplicativo3(p):
    'TermoMultiplicativo : TermoMultiplicativo MOD Fator'
    type1 = get_expr_type(p[1])
    type2 = get_expr_type(p[3])
    
    if not parser.semantic_analyzer.check_arithmetic_operation(type1, type2, 'mod', p.lineno(2)):
        parser.success = False
        p[0] = ""
        return
    
    code = generate_expr_code(p[1]) + generate_expr_code(p[3]) + "mod\n"
    
    result_type = 'integer'
    p[0] = (result_type, code)

def p_termomultiplicativo4(p):
    'TermoMultiplicativo : Fator'
    p[0] = p[1]

def p_fator1(p):
    'Fator : ID'
    var_name = p[1]
    if var_name in parser.symbol_table:
        mark_variable_used(var_name)
        p[0] = var_name
    else:
        if not parser.semantic_analyzer.check_variable_declaration(var_name, p.lineno(1)):
            parser.success = False
            p[0] = ""
            return

def p_fator2(p):
    'Fator : NUMBER'
    if isinstance(p[1], int):
        p[0] = ('integer', f"pushi {p[1]}\n")
    else:
        p[0] = ('real', f"pushf {p[1]}\n")

def p_fator3(p):
    'Fator : STRING'
    p[0] = ('string', p[1])

def p_fator4(p):
    'Fator : TRUE'
    code = "pushi 1\n"
    p[0] = ('boolean', code)

def p_fator5(p):
    'Fator : FALSE'
    code = "pushi 0\n"
    p[0] = ('boolean', code)

def p_fator6(p):
    'Fator : LPAREN Expr RPAREN'
    p[0] = p[2]

def p_fator7(p):
    'Fator : ID LBRACKET Expr RBRACKET'
    var_name = p[1]
    if not parser.semantic_analyzer.check_variable_declaration(var_name, p.lineno(1)):
        parser.success = False
        p[0] = ""
        return
    elif parser.symbol_table[var_name]['type'] == 'string' and not parser.semantic_analyzer.check_string_access(var_name, get_expr_type(p[3]), p[3], p.lineno(1)):
        parser.success = False

    elif isinstance(parser.symbol_table[var_name]['type'], tuple) and not parser.semantic_analyzer.check_array_bounds(var_name, get_expr_type(p[3]), p[3], p.lineno(1)):
        parser.success = False

    mark_variable_used(var_name)
    p[0] = (var_name, p[3])

def p_fator8(p):
    'Fator : ID DOT ID'
    var_name = p[1]
    if var_name in parser.symbol_table:
        mark_variable_used(var_name)
        p[0] = var_name
    else:
        if not parser.semantic_analyzer.check_variable_declaration(var_name, p.lineno(1)):
            parser.success = False
            p[0] = ""
            return

def p_fator9(p):
    'Fator : ID LPAREN ID RPAREN'
    var_name = p[3]
    if var_name in parser.symbol_table:
        mark_variable_used(var_name)
        code = f"pushg {parser.symbol_table[var_name]['address']}\n"
        code += "strlen\n"
        p[0] = code
    else:
        if not parser.semantic_analyzer.check_variable_declaration(var_name, p.lineno(1)):
            parser.success = False
            p[0] = ""
            return

def p_fator10(p):
    'Fator : CHAR'
    char_code = ord(p[1])
    p[0] = ('char', f"pushi {char_code}\n")

def p_listaargumentos1(p):
    'ListaArgumentos : Expr ListaArgumentosTail'
    p[0] = [p[1]] + p[2]

def p_listaargumentos2(p):
    'ListaArgumentos : empty'
    p[0] = []

def p_listaargumentostail1(p):
    'ListaArgumentosTail : COMMA Expr ListaArgumentosTail'
    p[0] = [p[2]] + p[3]

def p_listaargumentostail2(p):
    'ListaArgumentosTail : empty'
    p[0] = []
    
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Erro de sintaxe no token {p.type} ('{p.value}') na linha {p.lineno}")
        parser.success = False
    else:
        print("Erro de sintaxe: fim de arquivo inesperado")
        parser.success = False

def compile_code_to_EWVM(file, parser, input_string):
    parser.semantic_analyzer.print_errors()
    if parser.success:
        if(file.split('/')[2] != 'others'):
            output = f"../out/output_{file.split('/')[2]}"
        else:
            output = f"../out/others/output_{file.split('/')[3]}"
        with open(output, "w") as f:
            f.write(input_string)
        print("Parsing foi bem-sucedido!")
        print(f"Tabela de símbolos: {parser.symbol_table}")
        print(input_string)
    else:
        print("Parsing falhou - não foi possível gerar código")

def mark_variable_used(var_name):
    """Marca uma variável como utilizada"""
    if isinstance(var_name, tuple):
        parser.used_variables.add(var_name[0])
    elif isinstance(var_name, str):
        parser.used_variables.add(var_name)

def parse_file(file, parser):
    parser.semantic_analyzer = SemanticAnalyzer()
    parser.success = True
    parser.var_counter = 0
    parser.symbol_table = {}
    parser.label_counter = 0
    parser.used_variables = set()
    
    with open(file, 'r') as f:
        input_string = f.read()
    
    result = parser.parse(input_string)

    parser.semantic_analyzer.check_unused_variables(parser.used_variables)
    
    compile_code_to_EWVM(file, parser, result)

if __name__ == "__main__":
    parser = yacc.yacc()
    parse_file(sys.argv[1], parser)