import sys
import socket
import re

host = ''
port = int(sys.argv[1])

listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.bind((host, port))
listenSocket.listen(1)

print ('Web service online.')
print ('Port: ', port)

while True:
	Conn, Addr = listenSocket.accept();
	request = Conn.recv(1024)
	request = request.decode()
	print (request)

	pattern = re.compile(r'GET (.*) HTTP[ ]?/[ ]?(\d\.\d|\d)')
	parsedRequest = pattern.split(request);
	try :
            requestFileDirectory = parsedRequest[1]
            File_name = requestFileDirectory[1:]
            test = open(File_name)# this is for raising exception if the File_name not exist
            requestFile = open(File_name, 'rb')
            response = "\nHTTP/1.1 200 OK\r\n\r\n".encode()+bytes(requestFile.read())
            requestFile.close()
            Conn.send(response)
	except Exception:
            response ="\nHTTP/1.1 404 Not Found\n\n".encode()
            Conn.send(response)
	Conn.close()
