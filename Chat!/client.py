import socket
import threading

host = '172.29.103.178'
port = 12345

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #declarar um socket de internet e um objeto TCP
client.connect((host, port)) #conectando o cliente ao servidor

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else: 
                print(message)
                
        except:
            print("an erroer occurred!")
            client.close()
            break
            
            
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()