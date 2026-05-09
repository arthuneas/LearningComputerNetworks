import socket
import threading

host = 'localhost'
port = 12345

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #declarar um socket de internet e um objeto UDP
client.connect((host, port)) #conectando o cliente ao servidor

mensagem_entrada = f"JOIN:{nickname}"
client.send(mensagem_entrada.encode('ascii'))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
                
        except Exception as e:
            print(f"ocorreu um erro: {e}")
            client.close()
            break
            
            
def write():
    while True:
        try:
            message = f'{nickname}: {input("")}'
            client.send(message.encode('ascii'))
        except:
            break
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()