# serv_sock.py
import socket
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'tracker.txt')

# Definicao de uma variavel x para o menu da aplicacao
x = 1

# Define IP  e Porta
HOST = 'localhost'
PORT = 1111

# Faz a configuração do Socket com os protocolos IPV4/TCP e configura o IP e Porta
ObjSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def servidor():

    ObjSocket.bind((HOST, PORT))
    print("SERVIDOR ATIVO!\nEsperando conexao...")

    # Ouve a conexao na porta
    ObjSocket.listen(1)

    # Confirmo a conexao com o outro PC
    conexao, endereco = ObjSocket.accept()
    print('Conectado com:', endereco)

    # Cliente, neste ponto, estara enviando o nome do arquivo solicitado
    resposta = conexao.recv(1024)

    arq = open(resposta.decode(), 'rb')
    print(resposta.decode())
    # Mando o arquivo
    ObjSocket.sendfile(arq)

    # Fecho o arquivo
    arq.close()


def cliente():
    # Abro o arquivo
    print("\nInsira o nome (com extensão) do arquivo que deseja receber\n")
    nome_arquivo = input()

    # Procura no tracker
    tracker = open(my_file, 'r')
    print("\nPesquisando no tracker.....")

    # Executa um loop dentro do arquivo
    for line in tracker:
        # Le a linha do arquivo
        
        # Se essa linah tem o arquivo que preciso....
        separa = line.split()
        if(separa[0] == nome_arquivo):
            # Tracker retorna quem tem, lê host e porta
            hostArq = separa[1]
            portArq = separa[2]
            # Faço a conexao no IP e Porta
            # Estabelecer conexão com esse PC
            try:
                ObjSocket.connect((hostArq, int (portArq)))
                print('Conexão concluida!\n')
                ObjSocket.sendall(str.encode(nome_arquivo))
                # Receber o arquivo
                # Envio o arquivo solicitado
                while 1:
                    dados = ObjSocket.recv(1024)
                    if not dados:
                        break
                # Salvar o arquivo
                arq = open(nome_arquivo, 'wb')
                arq.write(dados)
                arq.close()
                # Atualiza o tracker
                # Fecho o tracker em modo de leitura
                tracker.close()
                # Abro o tracker em modo de atualização
                tracker = open('tracker.txt', 'a')
                print("\nAtualizando o tracker.....")
                tracker.write(nome_arquivo+' '+HOST+' '+PORT+'\n')
                tracker.close()

            except socket.error:
                print('\nConexão indisponivel, tentando outra conexao')


# Este while funciona como a main do PC. PC é setado sempre como servidor
# para que possa ficar sempre disponivel para transfeir arquivo

while x:
    print("====================================================")
    print("\n -> Pressione C para solicitar um arquivo")
    print("\n -> Pressione S para Servidor")
    print("\n -> Pressione X para sair da aplicação\n")
    opcao = input()

    if opcao == 'C' or opcao == 'c':
        cliente()
    elif opcao == 'S' or opcao == 's':
        servidor()
    elif opcao == 'X' or opcao == 'x':
        x = 0
