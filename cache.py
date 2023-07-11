# Alunos: Victor Matheus Alflen (vma18) e Wendel Caio Moro (wcm18)
# Atualizado em: 24/04/2022
# 
# Servidor de cache, que armazena as temperaturas e responde a requisicoes do cliente

import socket
import time
import json
import signal
from datetime import datetime

# Cria o socket 
cache = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configuracoes globais de endereco do servidor de cache
ip = "127.0.0.1"
cache_port = 10000

# Define os enderecoes dos servidores de temperatura
servers = {
    "resolute": { "ip": "127.0.0.1",  "port": 10001 },
    "chad": { "ip": "127.0.0.1",  "port": 10002 },
    "cairo": { "ip": "127.0.0.1",  "port": 10003 },
}

# Define a tabela de cache 
cache_table = {
    "resolute": ["", 0],
    "chad": ["", 0],
    "cairo": ["", 0],
}
expiration_time = 30

# Encerra o servidor de cache
def exit_program(signum, frame):
    print(f"\n\rExiting cache server")
    cache.close()
    exit(0)

# Requisita a temperatura para um servidor
def request_temperature(ip, server_port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((ip, server_port))
        server.send(bytes("get_temperature", "utf-8"))
        buffer = server.recv(1024)
        buffer = buffer.decode("utf-8")
        server.close()
        print(f"Data received: {buffer}")
        return buffer
    except:
        print("[ERROR] temperature server offline")
        return 'error'

# Confere se a entrada da cache ainda esta valida
def cache_valid(server_id, time):
    return time - cache_table[server_id][1] <= 0

def start_cache_server():
    
    # Coloca o socket para escutar requisicoes
    cache.bind((ip, cache_port))
    cache.listen(5)

    print(f"I am cache server. Running on {str(ip)}:{str(cache_port)}")

    while True:
        # Aceita uma conexao
        client, address = cache.accept()
        print(f"Connection Estabilished - {address[0]}:{address[1]}")

        # Recebe a requisicao
        string = client.recv(1024)
        string = string.decode("utf-8")
        now = int(time.time())

        print("Actual cache table:", cache_table)

        data = {}
        for key in servers:

            # Se a temperatura do servidor não foi requisitada, ignora
            if (string != "all" and string != key):
                continue

            print(f"[REQUEST] Temperature from {key} requested")

            # Confere a cache
            if (not cache_valid(key, now)):
                print(f"Cache invalid, requesting new data")  

                # Se o valor na cache expirou, entao requisita novo valor
                server_ip = servers[key]["ip"]
                server_port = servers[key]["port"]
                temperature = request_temperature(server_ip, server_port)

                if (temperature == "error"):
                    cache_table[key] = ["error", 0]
                else:
                    print(f"Cache updated for server {key}")
                    cache_table[key] = [temperature, int(time.time()) + expiration_time]
            else:
                print(f"Cache still valid for server {key}")

            # Obtem o valor da tabela de cache
            data[key] = cache_table[key][0]

        # Converte o json para string e envia para o cliente  
        message = json.dumps(data)
        client.send(bytes(message, "utf-8"))

        # Encerra a conexão
        client.close()

# Execucao principal
if __name__ == "__main__":
    now = datetime.now()
    print("-----------------------------------------------")
    print("Cache server started at:", now.strftime("%d/%m/%Y, %H:%M:%S"))
    print("-----------------------------------------------")

    signal.signal(signal.SIGINT, exit_program)
    start_cache_server()