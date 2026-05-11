import socket
import threading

host = 'localhost'
port = 12345


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #declarar um socket de internet e um objeto UDP
server.bind((host, port)) #conectar o socket a um endereço e porta específicos

clients = {} #declaramos um dicionário para cada cliente e outro para os apelidos dos clientes

def broadcast(message, senderAddress): #função para enviar mensagens para todos os clientes
    for clientAddress in clients:
        if clientAddress != senderAddress: #para todo cliente no vetor de clientes, envie a mensagem
            server.sendto(message, clientAddress)
            
print("Server is listening!")
            

while True:
    try:
        message, address = server.recvfrom(1024) #tente receber uma mensagem de 1024 bytes do cliente 
        decodeMessage = message.decode(('utf-8'))
        
        if decodeMessage.startswith("JOIN:"):
            nickname = decodeMessage.split(":")[1]
            clients[address] = nickname
            
            print(f"Conectado com {str(address)} como {nickname}")
            
            joinMsg = f"{nickname} joined the chat!"
            broadcast(joinMsg.encode('utf-8'), address)
            
            server.sendto("Connected to the server!".encode('utf-8'), address)
            
        else:
            broadcast(message, address)
    
    except Exception as e: #se houver um erro, o cliente provavelmente se desconectou
        print(f"Um erro ocorreu: {e}")
        pass