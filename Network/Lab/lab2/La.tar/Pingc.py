from socket import *
import sys
import time

#The function to caculate the min,max,avg time and the successful rate of transmition.
def detials(rtt,sent,received):
    num = len(rtt)
    min_time = min(rtt) if num > 0 else 0
    max_time = max(rtt) if num > 0 else 0
    avg_time = sum(rtt) / num if num > 0 else 0
    print("{} packets transmitted, {} received, {:.2f}% packet loss".format(sent,received, 100 - ((received/sent)*100)))
    print('min = {:.2f} ms, max = {:.2f} ms, avg = {:.2f} ms'.format(min_time,max_time,avg_time))
argv = sys.argv
if len(argv) != 3:
    #if arguments from the commend line do not follow the format below, Print message and exit
    print('Incorrect input,format: Python3 <host name/IP> <Port number>')
    sys.exit(1)
#the local host from commend line arguments
host = argv[1]
#port number
port = int(argv[2])
#create an UDP client socket
client_socket = socket(AF_INET,SOCK_DGRAM)
client_socket.settimeout(1)
seq_num = 0
#the list that store rtt time
rtt_list = []
received = 0
#loop for pinging 10 times
while seq_num < 10:
    seq_num += 1
    #data send to the server
    data ='PING {} {}\r\n'.format(seq_num,time.asctime(time.localtime()))
    try:
        Rtt_start = time.time()
        client_socket.sendto(data.encode(),(host,port))
        message,address = client_socket.recvfrom(1024)
        Rtt_end = time.time()
        received += 1
        rtt_time = (Rtt_end - Rtt_start)*1000
        rtt_list.append(rtt_time)
        print('ping to {}, seq = {}, rtt = {:.2f} ms'.format(address[0],seq_num,rtt_time))
    except:
        print('ping to {}, seq = {}, rtt = timeout'.format(argv[1],seq_num))
        continue
detials(rtt_list,seq_num,received)
#close the client socket
client_socket.close()
