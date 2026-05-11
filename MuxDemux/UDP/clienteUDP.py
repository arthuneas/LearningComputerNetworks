import socket
import threading

host = 'localhost'
port = 12345

serverAddress = (host, port)

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #declarar um socket de internet e um objeto UDP

mensagem = f"JOIN:{nickname}"
client.sendto(mensagem.encode('utf-8'), serverAddress)

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode('utf-8'))
                
        except Exception :
            print("Você saiu do chat.")
            break
            
            
def write():
    while True:
        text = input("")
        
        if text.strip().lower() == 'sair':
            client.close()
            break
        
        message = f'{nickname}: {text}'
        
        try:
            client.sendto(message.encode('utf-8'), serverAddress)
        except:
            break
        
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()