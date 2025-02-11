import sys
from colorama import Fore, Style

def somadorOnOFF(l):
    tamanho = len(l) # tamanho do texto a analisar
    counter = 0 # contador da soma
    flag = False # flag para saber se está ON ou OFF
    index = 0 # index para percorrer o texto
    aux = 0 # variavel auxiliar para guardar a sequencia de digitos
    negative = False # flag para saber se o numero é negativo
    
    while index < tamanho : # percorrer o texto
        if l[index] == "=": # dou print do resultado da soma
            print(f"{Fore.GREEN}Resultado da soma: {Style.RESET_ALL}{counter}")
            index += 1
        elif l[index] == "-" and index+1 < tamanho and l[index+1].isdigit() and flag: # ver se o sinal negativo é seguido de um digito
            negative = True
            index += 1
        elif l[index].isdigit() and flag: # se for um digito
            aux = 0
            while l[index].isdigit() and index < tamanho: # enquanto for um digito
                aux = aux*10 # como vou ter mais um digito, multiplico por 10 para garantir a nova casa 
                aux += int(l[index]) # adiciono o novo digito
                index += 1
            
            if negative: 
                aux = aux * -1 # se tiver um sinal negativo, multiplico por -1
            counter += aux
            negative = False
        elif l[index] == "o" or l[index] == "O": # verificar se existe a palavra ON 
            if index+1 < tamanho and  l[index+1] == "n" or l[index+1] == "N":
                flag = True 
                index += 2 # passa a frente os caracteres "on"
            elif index+2 < tamanho and (l[index+1] == "f" or l[index+1] == "F") and (l[index+2] == "f" or l[index+2] == "F"):
                flag = False
                index += 3 # passa a frente os caracteres "off"
            else:
                index += 1 # se nao for on nem off, passa a frente
        else:
            index += 1
    print()
    print(f"{Fore.BLUE}Resultado final da soma: {Style.RESET_ALL}{counter}")
    print()
    return counter


def main():
    print()
    print(f"{Fore.BLUE}==================================================================={Style.RESET_ALL}")
    print("Bem-vindo ao somadorOnOff! Escreva 'sair' para fechar o programa.")
    print(f"{Fore.BLUE}==================================================================={Style.RESET_ALL}")
    
    while True:
        print("Selecione uma opção:")
        print(f"{Fore.GREEN}1. {Style.RESET_ALL}Usar o somador")
        print(f"{Fore.RED}2. {Style.RESET_ALL}Sair")
        
        entrada = sys.stdin.readline().strip()
        
        if entrada == "1":
            print("Opção selecionada: Usar o somador")
            with open('input.txt', 'r') as file:
                content = file.read()
            somadorOnOFF(content)
        elif entrada == "2":
            print("A fechar programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()