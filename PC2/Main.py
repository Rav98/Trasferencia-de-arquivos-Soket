# client_sock.py
import socket

# Define IP  e Porta
HOST = 'localhost'
PORT = 57000

# Faz a configuração do Socket com os protocolos IPV4/TCP e configura o IP e Porta
ObjSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faço a conexao no IP e Porta
ObjSocket.connect((HOST, PORT))

# Abro o arquivo
arq = open('tracker.txt', 'rb')

# Mando o arquivo
ObjSocket.sendfile(arq)

# Fecho o arquivo
arq.close()
