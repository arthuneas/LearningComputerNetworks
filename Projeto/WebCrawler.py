import socket
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def requisicao(host, porta, caminho):
    #cria a conexão via socket, envia o get HTTP e retorna a resposta
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.settimeout(5.0)
    cliente.connect((host, porta))

    #a requisição http manual com as quebras de linha padrão do protocolo
    requisicao = f"GET {caminho} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

    #envia a requisição ao servidor convertendo a string em byte
    cliente.sendall(requisicao.encode('utf-8'))

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
        link = tag_a.get('href')
        if link:
            linkEncontrados.append(link)


    return linkEncontrados #retorna um vetor com todos os links encontrados



def pegarRedirecionamento(cabecalhos):
    #divide o bloco de cabeçalhos em uma lista de linhas
    linhas = cabecalhos.split("\r\n")

    for linha in linhas:
        #transformaremos o location para minusculo para conferir se algum header
        if linha.lower().startswith("location"):
            #pega tudo depois de location e divide nos primeiros dois pontos
            caminho = linha.split(":", 1)[1].strip()
            return caminho

    return None


#lógica do crawler
def crawler(host, porta, caminho_inicial):
    relatorio = []
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
            cabecalhos, status, html = processarResposta(resposta)
            print(f"     STATUS: {status}")
            
            #organiza o relatório e une com a descrição
            descricaoStatus = {200: "OK", 301: "Moved Permanently", 302: "Found", 400: "Bad Request", 404: "Not Found", 500: "Internal Server Error"}.get(status, "Outro")
            relatorio.append(f"URL: {caminhoAtual} | Status: {status} ({descricaoStatus})")

            #toma uma decisão baseada no status
            if status == 200:
                newLinks = extrairLink(html)
                print(f"     Encontrados {len(newLinks)} links nessa página")

                for link in newLinks:
                    #transforma caminho relativo em absoluto
                    caminhoAbsoluto = urljoin(caminhoAtual, link)
                    
                    #remove ancoras
                    caminhoLimpa = caminhoAbsoluto.split("#")[0]
                    
                    #verifica o dominio, se ele é o mesmo, e ignora links para outros sites
                    parsed = urlparse(caminhoLimpa)
                    if parsed.netloc == "" or parsed.netloc == host:
                        caminho = parsed.path
                        
                        if caminho.startswith("/") and caminho not in visitados and caminho not in fila:
                            fila.append(caminho)
                    

            elif status == 301 or status == 302:
                #procura onde o servidor vai redirecionar
                caminho = pegarRedirecionamento(cabecalhos)

                if caminho:
                    print(f"    Redirecionamento para: {caminho}")

                    #tratamento de caminhos relativos e absolutos
                    #se for em um caminho absoluto, outro site, ele vai dar erro. Pois o crawler vai tem um host definido
                    #por isso, é necesário realizr a garantia de que o site siga em um caminho relativo
                    if caminho.startswith("/"):
                        if caminho not in visitados and caminho not in fila:
                            fila.append(caminho) #adiciona o caminho para processamento na fila
                            print(f"    Caminho {caminho} está sendo redirecionado. ")

                    else:
                        print("     ignorando redirecionamento absoluto/externo")
                        
                else:
                    print("     redirecionamento recebido, mas não há cabeçalho Location")


            elif status == 404 or status == 500:
                print(f"Status: {status}\n")
                print("    Erro no servidor ou página não encontrada.")
                
                

        except Exception as e:
            print(f"Erro Geral: {e}")
            relatorio.append(f"URL: {caminhoAtual} | Status: ERRO ({e})")
            
    with open("relatorio_crawler.txt", "w", encoding="utf-8") as arquivo:
        for linha in relatorio:
            arquivo.write(linha + "\n")
    print("Relatório Gerado")

#execucao principal
if __name__ == "__main__":
    HOST = "info.cern.ch"
    PORTA = 80
    CAMINHO = "/hypertext/WWW/TheProject.html"

    crawler(HOST, PORTA, CAMINHO)