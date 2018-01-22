from socket import *
import os
import datetime
import codecs

MAX_cli = 1

class HTTPrequest:
    method = ''
    req_resource = ''
    HTTP_version = ''
    src_IP_addr = ''
    src_port = ''

    def __init__(self, method, req_resource, HTTP_version, Accept, src_IP_addr, src_port):
        self.method = method
        self.req_resource = req_resource
        self.HTTP_version = HTTP_version
        self.src_IP_addr = src_IP_addr
        self.src_port = src_port

class HTTPresponse:
    status_line = ''
    response_header = ''    # only the Date and time
    response_message_body = ''  # use the read method to extract all

    def __init__(self, status_line, response_header, response_body):
        self.status_line = status_line
        self.response_header = response_header
        self.response_body = response_body

def extractString(string):
    # 1 for In, 0 for not In
    IN = 1
    OUT = 0
    state = OUT
    newString = ''
    # Extract the string inside the single quote
    for ch in string:
        if state == OUT:
            if ch == "\'":
                state = IN
        elif state == IN:
            if ch == "\'":
                break
            else:
                newString += ch
    return newString


#   parsing the request to fit the HTTP request object
def parseHTTPrequest(string, addr):
    # 1 for In, 0 for not In
    temString = extractString(string)
    # Tokenize the string by line
    temList = []
    temList = temString.split('\\r\\n')

    requestLine = temList[0].split(' ')

    acceptType = ''
    for item in temList:
        if 'Accept' in item:
            accpetType = (item.split(' '))[1]
    httpRequest = HTTPrequest(requestLine[0], requestLine[1], requestLine[2], acceptType, addr[0], addr[1])
    return httpRequest


def main():
    serverPort = 8080
    serverSocket = socket (AF_INET, SOCK_STREAM)
    serverSocket.bind (('', serverPort))
    serverSocket.listen(MAX_cli)

    print ('The Web server is ready to receive')
    while 1:
        connSocket, addr = serverSocket.accept()
        request = connSocket.recv(1024)
        req = parseHTTPrequest(str(request), addr)

        # Look for resource
        t = datetime.date.today()
        try:
            # 200 OK
            status_code = '200 OK'
            #res_header = t.ctime()
            infile = open (str(str(os.getcwd()+req.req_resource)), "rb") # rb solve the encoding issue
            pre_response_body = infile.read()
            response_body = extractString(str(pre_response_body))
            time = t.timetuple()
            tempRelist = [status_code, str(time), response_body]
            msg = '\\r\\n'.join(tempRelist)
            connSocket.send(msg.encode())
            print ('200 OK sent has been sent to:', addr[0],':', addr[1])

        except:
            # 404 not found
            status_code = '404 Not Found'
            time = t.timetuple()
            response_body = 'Request resource not found'
            tempRelist = [status_code, str(time), response_body]
            msg = '\\r\\n'.join(tempRelist)
            connSocket.send(msg.encode())
            print ('404 Not Found has been sent to:', addr[0], ':', addr[1])

        connSocket.close()

if __name__ == "__main__":
    main()
