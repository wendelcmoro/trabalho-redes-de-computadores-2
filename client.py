# Alunos: Victor Matheus Alflen (vma18) e Wendel Caio Moro (wcm18)
# Atualizado em: 24/04/2022
# 
# Cliente que requisita as informacoes de temperatura para o servidor de cache

import socket
from datetime import datetime
import signal
import json

# Configuracoes globais de endereco do servidor de cache
ip = "127.0.0.1"
port = 10000

commands = ["resolute", "chad", "cairo", "all", "help"]

# Encerra o cliente
def exit_program(signum, frame):
    print(f"\n\rExiting client")
    exit(0)

# Exibe ajuda
def print_help():
    print("Select city to get temperature:")
    print("  resolute: Resolute, Canada")
    print("  chad: Chad, Chad")
    print("  cairo: Cairo, Egypt")
    print("  all: all cities")
    print("  help: show this message")

def run_client():

    print_help()
    
    # loop de execucao
    while (True):
        # Obtem a entrada do usuario
        try:
            string = input("[INPUT] Get temperature from: ")
        except:
            exit_program(None, None)

        string = string.lower()
        if (string not in commands):
            print(f"[ERROR] wrong option")
            continue
        elif (string == "help"):
            print_help()
            continue

        # Faz a conexão no socket do servidor de cache
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip, port))

            # Envia a requisicao
            client.send(bytes(string, "utf-8"))

            # Recebe os dados
            buffer = client.recv(1024)
            buffer = buffer.decode("utf-8")
            print(f"Cache server response: {buffer}")
        except:
            print(f"[ERROR] cache server unavailable")
            continue

        # Decodifica o json recebido
        try:
            response = json.loads(buffer)
        except json.JSONDecodeError:
            print(f"Cache server response is not a valid json, ignoring")
            continue

        for key in response:
            if (response[key] != 'error'):
                print(f"Temperature in {key}: {response[key]} °C")
            else:
                print(f"Temperature in {key} is unavailable")

        client.close()

# Execucao principal
if __name__ == "__main__":
    # Captura o sinal de ctrl-c para sair do programa sem erro
    signal.signal(signal.SIGINT, exit_program)
    
    now = datetime.now()
    print("---------------------------------------")
    print("Client started at:", now.strftime("%d/%m/%Y, %H:%M:%S"))
    print("---------------------------------------")

    # Executa o cliente
    run_client()