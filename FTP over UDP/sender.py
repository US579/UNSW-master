import socket
import time
import threading
import pickle
import sys,os
import math
import random
import hashlib

class Segment:
    def __init__(self,SYN = 0,ACK = 0, Fin = 0, seq = 0, ack = 0, data = '',checksum = 0,cur_time = 0.0):
        self.SYN = SYN
        self.ACK = ACK            #ack value :the next seqence number
        self.Fin = Fin            #fin flag use to justify the fin segemnt,it is for the termination
        self.seq = seq            #sequence number
        self.ack = ack            #acknowledge number
        self.data = data          #data
        self.checksum = checksum  #hex string that for checksum function
        self.cur_time = cur_time  #for calcuating the SampleRTT

def check_sum_send(seg):
    md5 = hashlib.md5()
    md5.update(pickle.dumps(seg))
    seg.checksum = md5.hexdigest()
    return seg

def check_sum_receive(seg):
    checksum = seg.checksum
    seg.checksum = 0
    md5 = hashlib.md5()
    md5.update(pickle.dumps(seg))
    check = md5.hexdigest()
    if check == checksum:
        return True
    return False


def PLD(reply_segment,host,port):
    global drop_num
    global duplicate_num
    global corrupt_num
    global reorder_num
    global delay_num
    global flag
    global reorder_segment
    global trans_num
    global PLD_num
    global flag_num
    global boom
    global start
    global reorder_list
    global sign


    PLD_num += 1
    drop_rate = random.random()
    duplicate_rate = random.random()
    corrupt_rate = random.random()
    reorder_rate = random.random()
    delay_rate = random.random()

    if trans_num - flag_num == maxOrder and boom == 0:
        print('transfer the reorder segments')
        trans_num += 1
        s.sendto(pickle.dumps(reorder_segment), (host, port))
        f.write('snd/rord                {:<.2f}   D    {:<5d}    {:<5d}    {:<5d}\n'.format((time.time() - start),
                                                                                         reorder_segment.seq,
                                                                                         len(reorder_segment.data),
                                                                                         reorder_segment.ack))
        boom = 1
        
    if flag:
        if reply_segment.ack in reorder_list:
            duplicate_num += 1
        trans_num += 1
        reply_segment = check_sum_send(reply_segment)
        s.sendto(pickle.dumps(reply_segment), (host, port))
        f.write('snd/RXT               {:<.2f}   D    {:<5d}    {:<5d}    {:<5d}\n'.format((time.time() - start),
                                                                                           reply_segment.seq,
                                                                                           len(reply_segment.data),
                                                                                           reply_segment.ack))
        flag = 0
        return

    if reply_segment.seq in reorder_list:
        return


    if drop_rate <= pDrop:
        print('drop packet')
        trans_num += 1
        drop_num +=1
        f.write('drop                  {:<.2f}   D    {:<5d}   {:<5d}    {:<5d}\n'.format((time.time() - start) ,
                                                                                          reply_segment.seq,
                                                                                          len(reply_segment.data),
                                                                                          reply_segment.ack))
        return

    if duplicate_rate <= pDuplicate:
        duplicate_num += 1
        print('duplicate packet')
        print('send seq number:', reply_segment.seq)
        reply_segment = check_sum_send(reply_segment)
        trans_num += 2
        s.sendto(pickle.dumps(reply_segment), (host, port))
        f.write('snd                   {:<.2f}   D    {:<5d}   {:<5d}     {:<5d}\n'.format((time.time() - start),
                                                                                           reply_segment.seq,
                                                                                           len(reply_segment.data),
                                                                                           reply_segment.ack))
        s.sendto(pickle.dumps(reply_segment), (host, port))
        f.write('snd/dup               {:<.2f}   D    {:<5d}   {:<5d}     {:<5d}\n'.format((time.time() - start) ,
                                                                                           reply_segment.seq,
                                                                                           len(reply_segment.data),
                                                                                           reply_segment.ack))
        return

    if corrupt_rate <= pCorrupt:
        print("corrupt packet")
        print('send seq number:', reply_segment.seq)
        trans_num += 1
        corrupt_num+=1
        reply_segment = check_sum_send(reply_segment)
        reply_segment.data = reply_segment.data[1:]
        s.sendto(pickle.dumps(reply_segment), (host, port))
        f.write('snd/corr              {:<.2f}   D    {:<5d}   {:<5d}     {:<5d}\n'.format((time.time() - start) ,
                                                                                             reply_segment.seq,
                                                                                             len(reply_segment.data),
                                                                                             reply_segment.ack))
        return
    if reorder_rate <= pOrder:
        if boom:
            print('packet reorder')
            print('send seq number:', reply_segment.seq)
            reorder_num += 1
            reorder_list.append(reply_segment.seq)
            reorder_segment = check_sum_send(reply_segment)
            flag_num = trans_num
            boom = 0
            return


    if delay_rate <= pDelay:
        print('packet delay')
        print('send seq number:', reply_segment.seq)
        delay_num+=1
        trans_num += 1
        time.sleep(random.uniform(0,maxDelay/1000))
        reply_segment = check_sum_send(reply_segment)
        s.sendto(pickle.dumps(reply_segment), (host, port))
        f.write('snd/dely               {:<.2f}   D    {:<5d}   {:<5d}     {:<5d}\n'.format((time.time() - start) ,
                                                                                             reply_segment.seq,
                                                                  len(reply_segment.data), reply_segment.ack))
        return
    print('send seq number:', reply_segment.seq)
    trans_num += 1
    reply_segment = check_sum_send(reply_segment)
    s.sendto(pickle.dumps(reply_segment), (host, port))
    f.write('snd                   {:<.2f}   D    {:<5d}   {:<5d}      {:<5d}\n'.format((time.time() - start), reply_segment.seq,
                                                                      len(reply_segment.data), reply_segment.ack))




def handshake():
    global start
    global client_isn
    global drop_num
    global error
    global trans_num
    hands = Segment(seq = client_isn,SYN=1,cur_time=time.time())
    hands = check_sum_send(hands)
    trans_num += 1
    s.sendto(pickle.dumps(hands),(receiver_host_ip,receiver_port))
    f.write('snd                   {:<.2f}   S    {:<5d}    {:<5d}      {:<5d}\n'.format((time.time()-start), client_isn,0,0))
    while True:
        data,address = s.recvfrom(2048)
        received_hey = pickle.loads(data)
        if check_sum_receive(received_hey):
            if received_hey.SYN == 1 and received_hey.ACK == 1 and received_hey.ack == client_isn + 1:
                client_isn += 1
                f.write('rcv                   {:<.2f}   SA  {:<5d}     {:<5d}       {:<5d}\n'.format((time.time() - start),
                                                                                    received_hey.seq,0, received_hey.ack))

                hands = Segment(ACK=1,ack=received_hey.seq + 1,seq=client_isn,cur_time=time.time())
                hands = check_sum_send(hands)
                trans_num += 1
                s.sendto(pickle.dumps(hands),address)
                f.write('snd                   {:<.2f}   A   {:<5d}     {:<5d}      {:<5d}\n'.format((time.time() - start) ,
                                                                                                 hands.seq,0,hands.ack))
                return received_hey.seq + 1
        else:
            error+=1
            trans_num += 1
            f.write('drop/corr       {:<.2f}    D   {:<5d}      {:<5d}     {:<5d}\n'.format((time.time() - start) ,
                                                                                                   received_hey.seq,
                                                                                                   len(received_hey.data),
                                                                                                   received_hey.ack))



def updateERTT():
    global SampleRTT
    global EstimatedRTT
    return 0.875 * EstimatedRTT + 0.125 * SampleRTT

def updateDRTT():
    global DevRTT
    global SampleRTT
    global EstimatedRTT
    DevRTT =0.75*DevRTT + 0.25*(abs(SampleRTT-EstimatedRTT))
    return DevRTT

def updatetimeout():
    global timeout_interval
    global EstimatedRTT
    global DevRTT
    global gamma
    EstimatedRTT = updateERTT()
    DevRTT = updateDRTT()
    timeout_interval = EstimatedRTT + (gamma * DevRTT)
    return timeout_interval


def receiverThreading():
    global sendbase
    global retransmit_num
    global last_ack
    global duplicate_num
    global drop_num
    global error
    global flag1
    global dup_ack
    global start
    global EstimatedRTT
    global timeout_interval
    global lis
    global gamma
    global SampleRTT

    while True:
        data,address = s.recvfrom(2048)
        received_segments = pickle.loads(data)
        if check_sum_receive(received_segments):
            if received_segments.ACK:
                if received_segments.ack in lis:
                    dup_ack +=1
                    f.write('rcv/DA                {:<.2f}    A   {:<5d}        {:<5d}    {:<5d}\n'.format(
                                                                                      (time.time() - start),
                                                                                       received_segments.seq, 0,
                                                                                      received_segments.ack))
                else:
                    f.write('rcv                   {:<.2f}    A    {:<5d}       {:<5d}    {:<5d}\n'.format((time.time() - start) ,
                                                                                                  received_segments.seq, 0,
                                                                                                  received_segments.ack))
                lis.append(received_segments.ack)
                if received_segments.ack > client_isn + MSS * sendbase:
                    print('received_segments.ack:',received_segments.ack)
                    if received_segments.cur_time:
                        SampleRTT = time.time() - received_segments.cur_time
                        timeout_interval = updatetimeout()
                    sendbase = math.ceil((received_segments.ack-client_isn)/MSS)
                    retransmit_num = 0
                elif received_segments.ack <= client_isn + MSS * sendbase:
                    retransmit_num += 1
            if sendbase >= len(buffer):
                last_ack = received_segments.ack
                break
        else:
            error +=1
            f.write('drop/corr       {:<.2f}    D    {:<5d}        {:<5d}     {:<5d}\n'.format((time.time() - start) ,
                                                                                               received_segments.seq,
                                                                                               len(received_segments.data),
                                                                                               received_segments.ack))



def transfer_windows():
    global buffer
    global sendbase
    global timer
    global cur_loc
    global retransmit_num
    global data_len,seg_amount
    with open(file_name,'rb') as f:
        f = f.read()
    data_len = len(f)
    #find how much segments can be generated
    seg_amount = math.ceil(data_len/MSS)
    #slice the file
    if f:
        for i in range(0,data_len,MSS):
            if i + MSS < data_len:
                buffer.append(f[i:i+MSS])
            else:
                buffer.append(f[i:])
    else:
        seg_amount = 1
        buffer = [b'']
    cur_loc = 0
    timer = time.time()
    for i in range(buff):
        if cur_loc >= len(buffer):
            cur_loc += 1
            break
        #print(cur_loc)
        segments = Segment(seq = client_isn + MSS*cur_loc,data=buffer[cur_loc],ack=ack,cur_time=time.time())
        #print(ack)
        cur_loc += 1
        PLD(segments,receiver_host_ip,receiver_port)





def senderThreading():
    global sendbase
    global timer
    global retransmit_num
    global cur_loc
    global fast_retran_num
    global timeout_retran_num
    global flag
    global timeout_interval

    while True:

        if cur_loc - sendbase < buff:
            timer = time.time()
            for i in range(sendbase + buff - cur_loc):
                if cur_loc >= len(buffer):
                    cur_loc = sendbase + buff
                    break
                reply_segemnts = Segment(ack=ack,seq =client_isn + MSS * cur_loc,data=buffer[cur_loc],cur_time=time.time())
                cur_loc += 1
                PLD(reply_segemnts,receiver_host_ip,receiver_port)
        if retransmit_num >= 3:
            reply_segemnts = Segment(data=buffer[sendbase],ack = ack,seq = client_isn + MSS*sendbase)
            fast_retran_num += 1
            flag = 1
            PLD(reply_segemnts,receiver_host_ip,receiver_port)
            retransmit_num = 0
        if time.time() - timer > timeout_interval:
            #timeout_interval = 2 * timeout_interval
            reply_segemnts = Segment(data=buffer[sendbase],ack = ack, seq = client_isn + MSS*sendbase)
            flag = 1
            timeout_retran_num += 1
            PLD(reply_segemnts,receiver_host_ip,receiver_port)
            timer = time.time()
        if sendbase >= len(buffer):
            break


def Fin_state():
    global last_ack
    global sendbase
    global trans_num
    global drop_num
    global error
    replay_segments = Segment(Fin=1,seq=last_ack,ack=ack,cur_time=time.time())
    replay_segments = check_sum_send(replay_segments)
    trans_num += 1
    s.sendto(pickle.dumps(replay_segments),(receiver_host_ip,receiver_port))
    f.write('snd                   {:<.2f}    F    {:<5d}        {:<5d}    {:<5d}\n'.format((time.time() - start),
                                                                                             replay_segments.seq, 0,
                                                                                             replay_segments.ack))

    while True:
        data,address = s.recvfrom(2048)
        received_segments = pickle.loads(data)

        if received_segments.Fin == 1 and received_segments.ACK == 1 and received_segments.ack == last_ack +1:
            last_ack += 1
            f.write('rcv                   {:<.2f}    A     {:<5d}        {:<5d}    {:<5d}\n'.format((time.time() - start) ,
                                                                          received_segments.seq, 0,
                                                                          received_segments.ack))
            f.write('rcv                   {:<.2f}    F    {:<5d}        {:<5d}    {:<5d}\n'.format(
                                                                            (time.time() - start),
                                                                            received_segments.seq, 0,
                                                                            received_segments.ack))

            replay_segments = Segment(ACK=1,ack=received_segments.seq + 1,seq = last_ack,cur_time=time.time())
            trans_num += 1
            s.sendto(pickle.dumps(replay_segments),address)
            f.write('snd                   {:<.2f}    A    {:<5d}        {:<5d}     {:<5d}\n'.format((time.time() - start) ,
                                                                                               replay_segments.seq, 0,
                                                                                              replay_segments.ack))
            break




if __name__ == '__main__':
    if len(sys.argv) != 15:
        print('WARNING:Not enough input parameters')
        sys.exit()
    #receiver IP and Port number
    receiver_host_ip, receiver_port  =sys.argv[1], int(sys.argv[2])
    #file name
    file_name = sys.argv[3]
    #print(receiver_port)
    # The maximum window size and Maximum Segment Size
    MWS, MSS = int(sys.argv[4]),int(sys.argv[5])
    #This value is used for calculation of timeout value.
    gamma = float(sys.argv[6])
    #The probability
    pDrop,pDuplicate, pCorrupt, pOrder=float(sys.argv[7]),float(sys.argv[8]),float(sys.argv[9]),float(sys.argv[10])
    #The maximum number of packets
    maxOrder, pDelay, maxDelay = int(sys.argv[11]),float(sys.argv[12]),int(sys.argv[13])
    #print(maxDelay)
    seed_num=int(sys.argv[14])
    random.seed(seed_num)

    buff = MWS//MSS #how many segments that can contains in one windows size
    sendbase =retransmit_num =drop_num =fast_retran_num = timeout_retran_num = trans_num = duplicate_num=corrupt_num=reorder_num= flag =\
    flag1=PLD_num=dup_ack  =flag_num =  delay_num =cur_loc =  0
    boom = 1

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print('connection..............')
    except:
        print("Fail to create")
        sys.exit()

    lis = []
    DevRTT = 0.25
    EstimatedRTT = 0.5
    timeout_interval =EstimatedRTT + (gamma*DevRTT)

    client_isn = 0
    f = open('Sender_log.txt', 'w')
    f.write('')
    f = open('Sender_log.txt', 'a')
    start = time.time()
    ack = handshake()
    buffer = list()
    reorder_segment = 0

    reorder_list = list()
    last_ack = 0
    error = 0
    sign = 1
    thread1 = threading.Thread(target=senderThreading)
    thread2 = threading.Thread(target=receiverThreading)
    thread2.start()
    transfer_windows()
    thread1.start()
    thread1.join()
    thread2.join()
    Fin_state()
    f.write('========================================================\n')
    f.write('Size of the file (in Bytes)                    {}\n'.format(data_len))
    f.write('Segments transmitted (including drop & RXT):   {}\n'.format(trans_num))
    f.write('Number of Segments handled by PLD              {}\n'.format(PLD_num))
    f.write('Number of Segments dropped                     {}\n'.format(drop_num))
    f.write('Number of Segments Corrupted                   {}\n'.format(corrupt_num))
    f.write('Number of Segments Re-ordered                  {}\n'.format(reorder_num))
    f.write('Number of Segments Duplicated                  {}\n'.format(duplicate_num))
    f.write('Number of Segments Delayed                     {}\n'.format(delay_num))
    f.write('Number of Retransmissions due to TIMEOUT       {}\n'.format(timeout_retran_num))
    f.write('Number of FAST RETRANSMISSION                  {}\n'.format(fast_retran_num))
    f.write('Number of DUP ACKS received                    {}\n'.format(dup_ack))
    f.write('========================================================')
    f.close()
    s.close()
