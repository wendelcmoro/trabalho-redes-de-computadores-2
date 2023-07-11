# Alunos: Victor Matheus Alflen (vma18) e Wendel Caio Moro (wcm18)
# Atualizado em: 24/04/2022
# 
# Servidor de temperatura, que gera uma temperatura aleatoria dentro da faixa escolhida para a cidade

import socket
from sys import argv
from random import randint
import signal
from datetime import datetime

# Cria o socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define os enderecos do servidores
servers = {
    "resolute": [ "127.0.0.1", 10001 ],
    "chad": [ "127.0.0.1", 10002 ],
    "cairo": [ "127.0.0.1", 10003 ],
}

# Define os dados para cada cidade
cities = {
    "resolute": { 
        "name" : "Resolute",
        "country" : "Canada",
        "max_temp" : -5, 
        "min_temp" : -40,
    },
    "chad": { 
        "name" : "Chad",
        "country" : "Chad",
        "max_temp" : 50, 
        "min_temp" : 20,
    },
    "cairo": { 
        "name" : "Cairo",
        "country" : "Egypt",
        "max_temp" : 50, 
        "min_temp" : 10,
    }
}

# Define a cidade que cada servidor ira prover, dependendo do parametro passado no inicio da execucao
server_name = argv[1]
if (server_name not in cities):
    print(f"\"{server_name}\" is not a known server, exiting")
    print("List of known servers: resolute, chad, cairo")
    exit(-1)

ip, port = servers[server_name]

# Encerra o servidor de temperatura
def exit_program(signum, frame):
    print(f"\n\rExiting temperature server - {cities[server_name]['name']}, {cities[server_name]['country']}")
    server.close()
    exit(0)

# Obtem uma temperatura aleatoria, dependendo da cidade definida
def get_temperature(data):
    if (data == "get_temperature"):
        max_temp = cities[server_name]["max_temp"]
        min_temp = cities[server_name]["min_temp"]
        return str(randint(min_temp * 100, max_temp * 100) / 100)
    
    return "error"

# Executa o cliente
def start_temp_server():

    # Coloca o socket para escutar requisicoes
    server.bind((ip, port))
    server.listen(5)

    print(f"I am server {server_name}. Running on {str(ip)}:{str(port)}")

    while True:
        # Aceita uma conecao
        client, address = server.accept()
        print(f"Connection Estabilished - {address[0]}:{address[1]}")

        # Recebe os dados
        data = client.recv(1024)
        data = data.decode("utf-8")
        print("Data received:", data)

        # Gera um valor de temperatura e converte para string
        message = get_temperature(data)
        print(f"Temperature got: {message} °C")
        
        # Devolve a temperatura para o servidor de cache
        client.send(bytes(message, "utf-8"))
        print(f"Temperature sent")

        # Encerra a conexão
        client.close()

# Execucao principal
if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_program)
    now = datetime.now()
    print("---------------------------------------")
    print(f"Starting temperature server - {cities[server_name]['name']}, {cities[server_name]['country']}")
    print("Temperature server started at:", now.strftime("%d/%m/%Y, %H:%M:%S"))
    print("---------------------------------------")
    start_temp_server()