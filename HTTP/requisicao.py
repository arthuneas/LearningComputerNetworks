'''
Agora vamos fazer uma requisição http via socket

Vamos implementar um cliente http usando socket, sendo assim, entendendo o protocolo na 
prática.

Uma requisição básica tem o formato: 
    GET /index.html HTTP/1.1
    Host: localhost
    
    sendo cada parte da requisição um significativo:
        -> GET → método HTTP
        -> /index.html → recurso solicitado
        -> HTTP/1.1 → versão
        -> Host → obrigatório no HTTP/1.1
        
Na execução do código será visto:
-> Status HTTP (ex: HTTP/1.1 200 OK)
-> Headers (Content-Type, Content-Length, etc.)
-> Corpo da resposta (HTML da página)
'''

import socket

HOST = "localhost"
PORT = 8080

request = "GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(request.encode())

    response = b""
    while True:
        data = s.recv(1024)
        if not data:
            break
        
        response += data

print(response.decode())