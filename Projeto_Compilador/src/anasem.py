class SemanticAnalyzer:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.symbol_table = {}
    
    def add_error(self, message, line=None):
        """Adiciona um erro semântico"""
        if line:
            self.errors.append(f"Linha {line}: {message}")
        else:
            self.errors.append(message)
    
    def add_warning(self, message, line=None):
        """Adiciona um warning semântico"""
        if line:
            self.warnings.append(f"Linha {line}: {message}")
        else:
            self.warnings.append(message)
    
    def set_symbol_table(self, symbol_table):
        """Define a tabela de símbolos do parser"""
        self.symbol_table = symbol_table
    
    def get_variable_type(self, var_name):
        """Obtém o tipo de uma variável da tabela de símbolos"""
        if var_name in self.symbol_table:
            return self.symbol_table[var_name]['type']
        return None
    
    def is_variable_declared(self, var_name):
        """Verifica se uma variável foi declarada"""
        return var_name in self.symbol_table
    
    def check_variable_declaration(self, var_name, line=None):
        """Verifica se uma variável foi declarada"""
        if not self.is_variable_declared(var_name):
            self.add_error(f"Variável '{var_name}' não foi declarada", line)
            return False
        return True
    
    def check_type_compatibility(self, type1, type2):
        """Verifica compatibilidade entre dois tipos"""
        if type1 == type2:
            return True
        
        if (type1 == 'integer' and type2 == 'real') or (type1 == 'real' and type2 == 'integer'):
            return True
        
        return False
    
    def check_assignment_compatibility(self, var_name, expr_type, line=None):
        """Verifica compatibilidade de atribuição"""
        if not self.check_variable_declaration(var_name, line):
            return False
        
        var_type = self.get_variable_type(var_name)
        
        if isinstance(var_type, tuple) and var_type[0] == 'array':
            var_type = var_type[3]  # tipo base do array
        
        if not self.check_type_compatibility(var_type, expr_type):
            self.add_error(f"Incompatibilidade de tipos: não é possível atribuir '{expr_type}' à variável '{var_name}' do tipo '{var_type}'", line)
            return False
        
        return True
    
    def check_array_access(self, var_name, index_type, line=None):
        """Verifica acesso a array"""
        if not self.check_variable_declaration(var_name, line):
            return False
        
        var_type = self.get_variable_type(var_name)
        
        if not isinstance(var_type, tuple) or var_type[0] != 'array':
            self.add_error(f"'Variável {var_name}' não é um array", line)
            return False
        
        if index_type != 'integer':
            self.add_error(f"Índice de array deve ser do tipo integer, recebido '{index_type}'", line)
            return False
        
        return True
    
    def check_string_access(self, var_name, index_type, index_term, line=None):
        """Verifica acesso a caractere de string"""
        if not self.check_variable_declaration(var_name, line):
            return False
        
        var_type = self.get_variable_type(var_name)
        
        if var_type != 'string':
            self.add_error(f"'{var_name}' não é uma string", line)
            return False
        
        if index_type != 'integer':
            self.add_error(f"Índice de string deve ser do tipo integer, recebido '{index_type}'", line)
            return False
        
        index_value = None
        print(self.symbol_table)
        if isinstance(index_term, tuple) and index_term[1].startswith("pushi "):
            index_var = index_term[1]
            index_value = int(index_var.split("pushi ")[1].strip())
        elif isinstance(index_term, str):
            return True
        
        if index_value is not None:
            size = len(self.symbol_table[var_name]['value'])
            if index_value < 0 or index_value >= size:
                self.add_error(f"Índice {index_value} fora dos limites da string '{var_name}' (tamanho {size})", line)
                return False
        
        return True
    
    def check_arithmetic_operation(self, left_type, right_type, operator, line=None):
        """Verifica operações aritméticas"""
        valid_types = ['integer', 'real']
        
        if left_type not in valid_types:
            self.add_error(f"Operação '{operator}': tipo '{left_type}' não é válido para operações aritméticas", line)
            return False
        
        if right_type not in valid_types:
            self.add_error(f"Operação '{operator}': tipo '{right_type}' não é válido para operações aritméticas", line)
            return False
        
        return True
    
    def check_logical_operation(self, left_type, right_type, operator, line=None):
        """Verifica operações lógicas"""
        if left_type != 'boolean':
            self.add_error(f"Operação '{operator}': operando esquerdo deve ser boolean, recebido '{left_type}'", line)
            return False
        
        if right_type != 'boolean':
            self.add_error(f"Operação '{operator}': operando direito deve ser boolean, recebido '{right_type}'", line)
            return False
        
        return True
    
    def check_comparison_operation(self, left_type, right_type, operator, line=None):
        """Verifica operações de comparação"""
        if not self.check_type_compatibility(left_type, right_type):
            self.add_error(f"Operação '{operator}': tipos incompatíveis '{left_type}' e '{right_type}'", line)
            return False
        
        return True
    
    def check_condition_type(self, expr_type, context, line=None):
        """Verifica se uma expressão pode ser usada como condição"""
        if expr_type != 'boolean':
            self.add_error(f"{context}: condição deve ser do tipo boolean, recebido '{expr_type}'", line)
            return False
        
        return True
    
    def check_for_loop_variable(self, var_name, line=None):
        """Verifica variável de controle do loop FOR"""
        if not self.check_variable_declaration(var_name, line):
            return False
        
        var_type = self.get_variable_type(var_name)
        
        if var_type != 'integer':
            self.add_error(f"Variável de controle do FOR deve ser do tipo integer, '{var_name}' é do tipo '{var_type}'", line)
            return False
        
        return True
    
    def check_for_loop_bounds(self, start_type, end_type, line=None):
        """Verifica limites do loop FOR"""
        if start_type != 'integer':
            self.add_error(f"Limite inicial do FOR deve ser integer, recebido '{start_type}'", line)
            return False
        
        if end_type != 'integer':
            self.add_error(f"Limite final do FOR deve ser integer, recebido '{end_type}'", line)
            return False
        
        return True
    
    def check_array_bounds(self, var_name, index_type, index_term, line=None):
        """Verifica se o índice está dentro dos limites do array"""
        if not self.check_variable_declaration(var_name, line):
            return False
        
        if not self.check_array_access(var_name, index_type, line):
            return False
        
        var_type = self.get_variable_type(var_name)

        index_value = None
        if isinstance(index_term, tuple) and index_term[1].startswith("pushi "):
            index_var = index_term[1]
            index_value = int(index_var.split("pushi ")[1].strip())
        elif isinstance(index_term, str):
            return True;

        if index_value is not None:
            min_index, max_index = var_type[1], var_type[2]
            if index_value < min_index or index_value > max_index:
                self.add_error(f"Índice {index_value} fora dos limites do array '{var_name}' [{min_index}..{max_index}]", line)
                return False
        
        return True
    
    def check_unused_variables(self, used_variables):
        """Verifica variáveis declaradas mas não utilizadas"""
        for var_name in self.symbol_table:
            if var_name not in used_variables:
                self.add_warning(f"Variável '{var_name}' declarada mas não utilizada")
    
    def print_errors(self):
        """Imprime todos os erros encontrados"""
        if self.errors:
            print("\n=== ERROS SEMÂNTICOS ===")
            for error in self.errors:
                print(f"ERRO: {error}")
            print("========================\n")
        
        if self.warnings:
            print("\n=== WARNINGS ===")
            for warning in self.warnings:
                print(f"WARNING: {warning}")
            print("==================\n")