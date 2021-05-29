# serv_sock.py
import socket

# Define IP  e Porta
HOST = 'localhost'
PORT = 57000

# Faz a configuração do Socket com os protocolos IPV4/TCP e configura o IP e Porta
ObjSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ObjSocket.bind((HOST, PORT))
print("SERVIDOR ATIVO!\nEsperando conexao...")

# Ouve a conexao na porta
ObjSocket.listen(1)

# Confirmo a conexao com o outro PC
conexao, endereco = ObjSocket.accept()
print('Conectado com:', endereco)

# Abro o arquivo que vou escrever os dados recebidos
arq = open('tracker.txt', 'wb')
print("Recebendo o arquivo...")

# Recebo e escrevo no arquivo. Termino quando o data for vazio
while 1:
    dados = conexao.recv(1024)
    if not dados:
        break
    arq.write(dados)

# Fecho o arquivo
arq.close()
# Fecho a conexao
conexao.close()
