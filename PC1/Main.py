# serv_sock.py
import socket

# Definicao de uma variavel x para o menu da aplicacao
x = 1

# Define IP  e Porta
HOST = 'localhost'
PORT = 57000

# Faz a configuração do Socket com os protocolos IPV4/TCP e configura o IP e Porta
ObjSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def servidor():
    # Menu provavelmente vem aqui
    
    ObjSocket.bind((HOST, PORT))
    print("SERVIDOR ATIVO!\nEsperando conexao...")

    # Ouve a conexao na porta
    ObjSocket.listen(1)

    # Confirmo a conexao com o outro PC
    conexao, endereco = ObjSocket.accept()
    print('Conectado com:', endereco)

    # Cliente, neste ponto, estara enviando o nome do arquivo solicitado
    resposta = conexao.recv(1024)

    # Abro o arquivo que vou enviar
    arq = open(resposta.decode(), 'rb')
    print("Enviando o arquivo...")

    # Envio o arquivo solicitado
    while 1:
        dados = conexao.recv(1024)
        if not dados:
            break
        arq.write(dados)
    
    # Fecha o arquivo
    arq.close()

# def encerrar(arq, conexao):
    # Fecho o arquivo
    # arq.close()
    # Fecho a conexao
    # conexao.close()

def cliente():
    # Abro o arquivo
    print ("\nInsira o nome (com extensão) do arquivo que deseja receber\n")
    nome_arquivo = input()

    # Procura no tracker
    # Tracker retorna quem tem, lê host e porta

    # Estabelecer conexão com esse PC

    # Receber o arquivo

    # Acrescentar no tracker que ele tem o arquivo

    # Faço a conexao no IP e Porta
    ObjSocket.connect((HOST, PORT))

    arq = open(nome_arquivo, 'rb')

    # Mando o arquivo
    ObjSocket.sendfile(arq)

    # Fecho o arquivo
    arq.close()

    # Depois de executar atividade de cliente, restaura status de servidor desta maquina
    servidor()
    

# Este while funciona como a main do PC. PC é setado sempre como servidor
# para que possa ficar sempre disponivel para transfeir arquivo

while x:
    servidor()
    print("====================================================")
    print("\n -> Pressione A para solicitar um arquivo")
    print("\n -> Pressione X para sair da aplicação\n")
    opcao = input()

    if opcao == 'A' or opcao == 'a':
        cliente()
    elif opcao == 'X' or opcao == 'x':
        x = 0
