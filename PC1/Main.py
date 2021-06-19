# serv_sock.py
import socket
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'tracker.txt')
listapcs = [1111, 2222]

# Definicao de uma variavel x para o menu da aplicacao
x = 1

# Define IP  e Porta
HOST = 'localhost'
PORT = 1111

# Faz a configuração do Socket com os protocolos IPV4/TCP e configura o IP e Porta
# ObjSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def servidor():
    ObjSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ObjSocket.bind((HOST, PORT))
    print("SERVIDOR ATIVO!\nEsperando conexao...")

    # Ouve a conexao na porta
    ObjSocket.listen(1)

    # Confirmo a conexao com o outro PC
    conexao, endereco = ObjSocket.accept()
    print('Conectado com:', endereco)

    # Cliente, neste ponto, estara enviando o nome do arquivo solicitado
    resposta = conexao.recv(1024)

    with open (resposta, 'rb') as file:
        for data in file.readlines():
            conexao.send(data)
    
    # Fechando conexão:
    ObjSocket.close()

def recebertracker():
    ObjSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ObjSocket.bind((HOST, PORT))
    print("\nEsperando conexao para atualização de tracker...")

    # Ouve a conexao na porta
    ObjSocket.listen(1)

    # Confirmo a conexao com o outro PC
    conexao, endereco = ObjSocket.accept()
    print('Conectado com:', endereco)

    # Recebimento do tracker:
    with open('tracker.txt', 'wb') as file:
        while(1):
            data = conexao.recv(1000000)
            if not data:
                break
            file.write(data)
    
    ObjSocket.close()

def cliente():
    ObjSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Abro o arquivo
    print("\nInsira o nome (com extensão) do arquivo que deseja receber\n")
    nome_arquivo = input()

    # Procura no tracker
    tracker = open(my_file, 'r')
    print("\nPesquisando no tracker.....")

    # Executa um loop dentro do arquivo
    for line in tracker:
        # Le a linha do arquivo
        
        # Se essa linha tem o arquivo que preciso....
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
                # Envio o arquivo solicitado
                with open(nome_arquivo, 'wb') as file:
                    while(1):
                        data = ObjSocket.recv(1000000)
                        if not data:
                            break
                        file.write(data)
                ObjSocket.close()
                # Atualiza o tracker
                # Fecho o tracker em modo de leitura
                tracker.close()
                # Abro o tracker em modo de atualização
                tracker = open('tracker.txt', 'a')
                print("\nAtualizando o tracker.....")
                tracker.write('\n'+nome_arquivo+' '+ str (HOST)+' '+str (PORT))
                tracker.close()
                # Compartilhar o tracker entre todos os computadores da rede
                print("\nTracker atualizado. Tracker será compartilhado com os computadores da rede.")
                cont = 0 # Contador do vetor de pcs
                for n in listapcs:
                    # Solicitamos que todos os demais computadores estejam em modo servidor para que possam receber tracker atualizado
                    continuar = 'n'
                    print("\nColoque todos os demais computadores em modo de RECEBIMENTO DE TRACKER. Digite S quando concluir.")
                    continuar = input();
                    # Após confirmação do usuário:
                    if continuar == 's' or continuar == 'S':
                        cont = cont + 1
                        if n != PORT:
                            try:
                                print("Valor de n: ", n)
                                # Conexão com o computador:
                                ObjSocket.connect((hostArq, 1111))
                                print('Conexão concluída com pc', cont)
                                # Envio do tracker:
                                with open (my_file, 'rb') as file:
                                    for data in file.readlines():
                                        ObjSocket.send(data)
                                ObjSocket.close()
                            except socket.error:
                                print("\nErro de conexão")
                break
            except socket.error:
                print('\nConexão indisponivel, tentando outra conexao')


# Este while funciona como a main do PC. PC é setado sempre como servidor
# para que possa ficar sempre disponivel para transfeir arquivo

while x:
    print("====================================================")
    print("\n -> Pressione C para solicitar um arquivo")
    print("\n -> Pressione S para Servidor")
    print("\n -> Pressione T para receber tracker atualizado")
    print("\n -> Pressione X para sair da aplicação\n")
    opcao = input()

    if opcao == 'C' or opcao == 'c':
        cliente()
    elif opcao == 'S' or opcao == 's':
        servidor()
    elif opcao =='T' or opcao == 't':
        recebertracker()
    elif opcao == 'X' or opcao == 'x':
        x = 0
