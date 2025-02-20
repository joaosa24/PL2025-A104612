import re
from colorama import Fore, Style

# REGEX PARA SEPARAR OS REGISTROS
LINE_SPLIT_REGEX = r'\n(?=(?:[^"]*"[^"]*")*[^"]*$)'

# REGEX PARA SEPARAR OS CAMPOS DE CADA REGISTRO
FIELD_SPLIT_REGEX = r'(?:[^;"]|"(?:[^"]|"")*")+'

def open_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        header = file.readline()  # Ignorar o cabeçalho
        data = file.read()  # Ler todo o conteúdo do arquivo
    return data

def parser(data):
    composers = set()
    works_per_period = {}
    titles_per_period = {}
    
    entries = re.split(LINE_SPLIT_REGEX, data)
        
    for entry in entries:
        fields = re.findall(FIELD_SPLIT_REGEX, entry)
        try:
            title, _, _, period, composer, *_ = fields # Ignore unnecessary fields and assign fields to variables
        except ValueError: # Ignore entries with missing fields
            continue
            
        if composer: # Ignore entries without composer
            composers.add(composer) 
            
            works_per_period.setdefault(period, 0) # Initialize the works counter per period
            works_per_period[period] += 1 # Increment the works counter per period
            
            titles_per_period.setdefault(period, []).append(title) # Add the title to the list of titles per period
            titles_per_period[period].sort() # Sort the list of titles per period

    return sorted(composers), works_per_period, titles_per_period

def handle_outputs(composers, works_per_period, titles_per_period):
    print("               " + Fore.YELLOW + "=" * 20 + Fore.RESET)
    print("                 Parsing de obras")
    print("               " + Fore.YELLOW + "=" * 20 + Style.RESET_ALL + "\n")

    with open('Composers.txt', 'w', encoding='utf-8') as file:
        file.write("Compositores:\n\n")
        file.writelines(f'{comp}\n' for comp in composers)
    print(Fore.GREEN + 'As informações relativas aos compositores foram guardadas com sucesso. (Composers.txt)' + Style.RESET_ALL + '\n')
    
    with open('WorksPerPeriod.txt', 'w', encoding='utf-8') as file:
        file.write("Obras por período:\n\n")
        file.writelines(f'{periodo}: {quantidade}\n' for periodo, quantidade in works_per_period.items())
    print(Fore.GREEN + 'As informações relativas às obras por período foram guardadas com sucesso. (WorksPerPeriod)' + Style.RESET_ALL + '\n')
    
    with open('TitlesPerPeriod.txt', 'w', encoding='utf-8') as file:
        file.write("Títulos por período:\n\n")
        file.writelines(f'{periodo}: {", ".join(titulos)}\n' for periodo, titulos in titles_per_period.items())
    print(Fore.GREEN + 'As informações relativas aos títulos por período foram guardadas com sucesso. (TitlesPerPeriod.txt)' + Style.RESET_ALL + '\n')
    
    user_input = input(f"Deseja visualizar os resultados? ({Fore.GREEN}s{Style.RESET_ALL}/{Fore.RED}n{Style.RESET_ALL}): \n")
    if user_input.lower() == 's':
        print(Fore.CYAN + 'Compositores: ' + Fore.RESET + ', '.join(composers), "\n")
        print(Fore.RED + 'Obras por período: ' + Fore.RESET +  str(works_per_period), "\n")
        print(Fore.BLUE + 'Títulos por período: ' + Fore.RESET + str(titles_per_period), "\n")
        print('Resultados visualizados com sucesso.' + Style.RESET_ALL + '\n')
    else: 
        print("\nPrograma concluído")

def main():
        data = open_csv('obras.csv')
        compositores, obra_por_periodo, titulos_periodo = parser(data)
        handle_outputs(compositores, obra_por_periodo, titulos_periodo)

if __name__ == '__main__':
    main()
