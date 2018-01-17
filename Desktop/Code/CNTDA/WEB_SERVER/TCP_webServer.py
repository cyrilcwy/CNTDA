class HTTPrequest:
    method = ''
    req_resource = ''
    HTTP_version = ''
    src_IP_addr = ''
    src_port = ''

    def __init__(self, method, req_resource, HTTP_version, src_IP_addr, src_port):
        self.method = method
        self.req_resource = req_resource
        self.HTTP_version = HTTP_version
        self.src_IP_addr = src_IP_addr
        self.src_port = src_port

from socket import *
MAX_cli = 10

serverPort = 8080
serverSocket = socket (AF_INET, SOCK_STREAM)
serverSocket.bind (('', serverPort))
serverSocket.listen(MAX_cli)

print ('The Web server is ready to receive')
while 1:
    connSocket, addr = serverSocket.accept()
    #request = str(connSocket.recv(1024)).split('\r\n')
    request = connSocket.recv(1024)

    print (request)

    connSocket.close()
