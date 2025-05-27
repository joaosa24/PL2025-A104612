from VendingMachine import VendingMachine
from datetime import date

def main():
    machine = VendingMachine()
    today = date.today().strftime("%Y-%m-%d")
    print(f"maq: {today}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")
    
    while True:
        command = input(">> ").strip().upper()
        if command == "SAIR":
            machine.return_change()
            print("maq: Até à próxima")
            break
        machine.process_command(command)

if __name__ == "__main__":
    main()
