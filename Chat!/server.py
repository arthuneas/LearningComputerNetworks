import socket
import threading

host = '127.0.0.1'
port = 12345


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #declarar um socket de internet e um objeto TCP
server.bind((host, port)) #conectar o socket a um endereço e porta específicos
server.listen() #o servidor procura novas conexões

clients = [] #declaramos um vetor para cada cliente e outro para os apelidos dos clientes
nicknames = []

def broadcast(message): #função para enviar mensagens para todos os clientes
    for client in clients:
        client.send(message) #para todo cliente no vetor de clientes, envie a mensagem
        
def handle(client): #função para lidar com mensagens de um cliente específico
    while True:
        try:
            message = client.recv(1024) #tente receber uma mensagem de 1024 bytes do cliente 
            broadcast(message) #envie a mensagem para todos os clientes
        
        except: #se houver um erro, o cliente provavelmente se desconectou
            index = clients.index(client) #encontre o índice no vetor do cliente que se desconectou
            clients.remove(client) #remova o cliente do vetor de clientes
            client.close() #feche a conexão com o cliente
            nickname = nicknames[index] #encontre o apelido no vetor na posição index do cliente que se desconectou
            broadcast(f'{nickname} left the chat!'.encode('ascii')) #envie uma mensagem para todos os clientes informando que o cliente se desconectou
            nicknames.remove(nickname) #remova o apelido do vetor de apelidos
            break
        
        
def receive(): #função para receber conexões de clientes
    while True:
        client, address = server.accept() #aceite uma nova conexão de cliente
        print(f'Connected with {str(address)}') #imprima o endereço do cliente que se conectou
        
        client.send('NICK'. encode('ascii')) #A primeira mensagem a ser enviada ao servidor será o nickname
        nickname = client.recv(1024).decode(('ascii')) #o cliente deve digitar, em até 1024 bytes/characteres, o seu nickname
        clients.append(client) #adiciona a resposta ao vetor de clientes
        nicknames.append(nickname) #adiciona o nickname ao vetor de nicknames
        
        print(f'the nickname of client {client} is {nickname}!') 
        broadcast(f'{nickname} joined the chat!.'.encode('ascii')) #indicamos efetivamente a entrada do client no chat
        client.send(f'Connectd to the server!'.encode('ascii')) #mostramos para todos os clientes do servidor que esse detemrinado cliente está conectado
        
        thread = threading.Thread(target=handle, args=(client,)) #criaremos threads para lidar com muitos clientes em um único servidor. Uma thread por cliente.
        thread.start() #inicializa a thread
        
if __name__ == '__main__':
    print("server is listening!")
    receive()
        