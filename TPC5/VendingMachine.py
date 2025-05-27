import json
import ply.lex as lex
from Product import Product

class VendingMachine:
    def __init__(self):
        self.stock = []
        self.balance = 0
        self.load_stock()
        self.lexer = None
        self.setup_lexer()
        
    def setup_lexer(self):
        # Token names
        tokens = (
            'LISTAR',
            'MOEDA',
            'SELECIONAR',
            'SAIR',
            'COIN',
            'PRODUCT_CODE',
            'COMMA',
            'DOT'
        )
        
        # Token rules
        t_LISTAR = r'LISTAR'
        t_MOEDA = r'MOEDA'
        t_SELECIONAR = r'SELECIONAR'
        t_SAIR = r'SAIR'
        t_COIN = r'\d+[eEc]'
        t_PRODUCT_CODE = r'[A-Z]\d+'
        t_COMMA = r','
        t_DOT = r'\.'
        
        # Ignored characters
        t_ignore = ' \t'
        
        def t_error(t):
            print(f"Caractere ilegal '{t.value[0]}'")
            t.lexer.skip(1)
            
        # Build the lexer
        self.lexer = lex.lex()
    
    def load_stock(self):
        try:
            with open("stock.json", "r") as f:
                data = json.load(f)
                self.stock = [Product(**item) for item in data]
        except FileNotFoundError:
            self.stock = []
            
    def save_stock(self):
        with open("stock.json", "w") as f:
            json.dump([vars(product) for product in self.stock], f, indent=4)
            
    def process_command(self, command):
        self.lexer.input(command)
        tokens = list(iter(self.lexer.token, None))
        
        if not tokens:
            print("maq: Comando inválido")
            return
            
        first_token = tokens[0]
        
        if first_token.type == 'LISTAR':
            self.list_products()
        elif first_token.type == 'MOEDA':
            coins = []
            for tok in tokens[1:]:
                if tok.type == 'COIN':
                    coins.append(tok.value)
            self.add_coins(coins)
        elif first_token.type == 'SELECIONAR':
            if len(tokens) > 1 and tokens[1].type == 'PRODUCT_CODE':
                self.select_product(tokens[1].value)
            else:
                print("maq: Código de produto inválido")

    def list_products(self):
        print("maq:")
        format_str = "{:<6} | {:<15} | {:<12} | {:<8}"
        print(format_str.format("COD", "NOME", "QUANTIDADE", "PREÇO"))
        print("-" * 47)
        for product in self.stock:
            preco_cents = int(product.preco * 100)
            print(format_str.format(
                product.cod,
                product.nome,
                str(product.quant),
                f"{preco_cents}"
            ))

    def add_coins(self, coins):
        coins_added = 0
        for coin in coins:
            value = int(coin[:-1])
            unit = coin[-1].lower()
            
            if unit == 'e':
                self.balance += value * 100
            else:  # unit == 'c'
                self.balance += value
            coins_added += 1

        print(f"maq: Recebi {coins_added} moedas.")
        self._print_balance()

    def _print_balance(self):
        euros = self.balance // 100
        cents = self.balance % 100
        if euros > 0:
            if cents > 0:
                print(f"maq: Saldo = {euros}e{cents:02d}c")
            else:
                print(f"maq: Saldo = {euros}e")
        else:
            print(f"maq: Saldo = {cents}c")

    def select_product(self, code):
        for product in self.stock:
            if product.cod == code:
                if product.quant > 0:
                    preco_cents = int(product.preco * 100)
                    if self.balance >= preco_cents:
                        product.quant -= 1
                        self.balance -= preco_cents
                        print(f'maq: Pode retirar o produto dispensado "{product.nome}"')
                        self._print_balance()
                        self.save_stock()
                        return
                    else:
                        print("maq: Saldo insuficiente para satisfazer o seu pedido")
                        print(f"maq: Saldo = {self.balance//100}e{self.balance%100}c; Pedido = {preco_cents}c")
                        return
                else:
                    print("maq: Produto esgotado")
                    return
        print("maq: Produto não existe")
        
    def return_change(self):
        coins = [200, 100, 50, 20, 10, 5, 2, 1]
        change = {}
        remaining = self.balance
        
        for coin in coins:
            if remaining >= coin:
                count = remaining // coin
                change[coin] = count
                remaining -= count * coin
                
        if change:
            change_str = ", ".join([f"{count}x {coin//100}e" if coin >= 100 else f"{count}x {coin}c" 
                                    for coin, count in change.items()])
            print(f"maq: Pode retirar o troco: {change_str}")
        self.balance = 0
