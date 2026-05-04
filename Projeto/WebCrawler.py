import socket
from bs4 import BeautifulSoup

def requisicao(host, porta, caminho):
    #cria a conexão via socket, envia o get HTTP e retorna a resposta
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, porta))
    
    #a requisição http manual com as quebras de linha padrão do protocolo
    requisicao = f"GET {caminho} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    
    #envia a requisição ao servidor convertendo a string em byte
    cliente.sendall(requisicao.encode('uft-8'))
    
    #recebe a resposta aos poucos até o servidor fechar a conexão
    respostaBruta = b""
    while True:
        pedaco = cliente.recv(4096)
        if not pedaco:
            break
        
        respostaBruta += pedaco
        
        
    cliente.close()
    
    return respostaBruta.decode('utf-8', errors='ignore')



#separar cabeçalho do corpo
def processarResposta(respostaBruta):
    #separa o cabeçalho do html e descobre o código de status HTTP
    
    partes = respostaBruta.split("\r\n\r\n", 1)
    
    cabecalhos = partes[0]
    html = partes[1] if len(partes) > 1 else ""
    
    #pega a primeira linha (HTTP/1.1 200 OK)
    primeiraLinha =  cabecalhos.split("\r\n")[0]
    
    status = int(primeiraLinha.split(" ")[1])
    
    return cabecalhos, status, html



    
#extraindo os links com bs4
def extrairLink(html):
    #le o html, acha as tags <a> e devolve uma lista com os hrefs
    soup = BeautifulSoup(html, 'html.parser')
    linkEncontrados = []
    
    #busca as tags de âncora
    for tag_a in soup.find_all('a'):
        link = tag_a.get('h_ref') 
        if link:
            linkEncontrados.append(link)
            
    
    return linkEncontrados #retorna um vetor com todos os links encontrados



#lógica do crawler
def crawler(host, porta, caminho_inicial):
    fila = [caminho_inicial]
    visitados = set() #não aceita duplicatas na checagem da lista
    
    
    while fila: 
        caminhoAtual = fila.pop(0) #tira o primeiro elemento da fila
        
        if caminhoAtual in visitados:
            continue
        
        print(f"Caminho Atual: {caminhoAtual}")
        visitados.add(caminhoAtual)
        
        
        try:
            #primeiro baixa a página
            resposta = requisicao(host, porta, caminhoAtual)
            
            #resposta do servidor
            status, cabecalhos, html = processarResposta(resposta)
            print(f"     STATUS: {status}")
            
            #toma uma decisão baseada no status
            if status == 200:
                newLinks = extrairLink(html)
                print(f"     Encontrados {len(newLinks)} links nessa página")
                
                fila.extend(newLinks)
                
            if status == 301 or status == 302:
                print
                
            if status == 404 or status == 500: 
                print("    Erro no servidor ou página não encontrada.")
                
        except Exception as e:
            print("Erro Geral: {e}")


#execucao principal
if __name__ == "__main__":
    HOST = ""
    PORTA = 20
    
    crawler(HOST, PORTA, "/")