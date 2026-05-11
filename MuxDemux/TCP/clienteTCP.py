import socket
import threading

host = 'localhost'
port = 12345

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #declarar um socket de internet e um objeto TCP
client.connect((host, port)) #conectando o cliente ao servidor

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else: 
                print(message)
                
        except:
            print("Você se desconectou do chat.")
            client.close()
            break
            
            
def write():
    while True:
        text = input("")
        
        if text.strip().lower() == 'sair':
            client.close()
            break
        
        message = f'{nickname}: {text}'
        
        try:
            client.send(message.encode('utf-8'))
        except:
            break
        
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()