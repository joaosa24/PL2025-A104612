from calc_anasin import rec_Parser

def main():
    while True:
        try:
            text = input('calc> ')
            if text.lower() == 'quit':
                break
            ast = rec_Parser(text)
            result = ast.eval()
            print(f'= {result}')
        except Exception as e:
            print(f'Erro: {str(e)}')

if __name__ == '__main__':
    main()
