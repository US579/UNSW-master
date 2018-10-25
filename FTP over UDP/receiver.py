import pickle
import socket,time
import hashlib,sys



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

def next_seq(dic):
    seq_list = sorted(dic)
    if seq_list[0] != first_ack:
        return first_ack
    for i in range(1,len(dic)):
        if seq_list[i] - seq_list[i-1] != len(dic[seq_list[i-1]]):
            return seq_list[i-1] + len(dic[seq_list[i-1]])
    return seq_list[-1] + len(dic[seq_list[-1]])


def handshake():
    global server_isn
    global start
    global seg_num
    global drop_num
    while True:
        data,address = s.recvfrom(2048)
        if not data:
            break
        seg_num += 1
        received_hey = pickle.loads(data)
        if check_sum_receive(received_hey):
            if received_hey.SYN == 1:
                with open('Receiver_log.txt', 'a') as f:
                    f.write('rcv   {:<.2f} S   {:<d}  {:<d}  {:<d}\n'.format((time.time() -start), received_hey.seq, 0,received_hey.ack))
                hands = Segment(SYN=1,ACK=1,seq=server_isn,ack=received_hey.seq+1)
                hands = check_sum_send(hands)

                s.sendto(pickle.dumps(hands),address)
                with open('Receiver_log.txt', 'a') as f:
                    f.write('snd   {:<.2f} SA  {:<d}  {:<d}  {:<d}\n'.format((time.time() - start), received_hey.seq, 0,received_hey.ack))
                continue
            if received_hey.ACK == 1:
                with open('Receiver_log.txt', 'a') as f:
                    f.write('rcv   {:<.2f}  A   {:<d}  {:<d}  {:<d}\n'.format((time.time() - start), received_hey.seq,0, received_hey.ack))
                server_isn += 1
                return received_hey.seq
        else:
            drop_num += 1
            with open('Receiver_log.txt', 'a') as f:
                f.write('drop/corr   {:<.2f}    D   {:<d}  {:<d}  {:<d}\n'.format((time.time() - start) ,
                                                                                        received_hey.seq,
                                                                                        len(received_hey.data),
                                                                                        received_hey.ack))


def transfer_state():
    global server_isn
    global seg_num
    global error
    global lis
    global dup_ack
    global count_duplicate

    seq_dict = dict()
    data_len = 0
    #count_duplicate = 0
    data_contain = 0
    while True:
        data,address = s.recvfrom(2048)
        if not data:
            break
        seg_num += 1
        received_segments = pickle.loads(data)

        if check_sum_receive(received_segments):

            if received_segments.data:
                data_contain += 1
                with open('Receiver_log.txt', 'a') as f:
                    f.write('rcv    {:<.2f}   D   {:<d}  {:<d}  {:<d}\n'.format((time.time() - start), received_segments.seq,
                                                                        len(received_segments.data), received_segments.ack))
                if received_segments.seq not in seq_dict:
                    seq_dict[received_segments.seq] = received_segments.data
                    data_len += len(received_segments.data)
                    ack = next_seq(seq_dict)
                    reply_segemnts = Segment(ACK=1,seq=server_isn,cur_time=received_segments.cur_time)
                    if received_segments.data:
                        reply_segemnts.ack = ack
                    else:
                        reply_segemnts.ack = ack + 1
                    reply_segemnts = check_sum_send(reply_segemnts)
                    s.sendto(pickle.dumps(reply_segemnts),address)
                    with open('Receiver_log.txt', 'a') as f:
                        if lis[-1] == ack:
                            dup_ack += 1
                            f.write('snd/DA {:<.2f}   A    {:<d}  {:<d}  {:<d}\n'.format((time.time() - start) ,
                                                                                            reply_segemnts.seq,0,
                                                                                             reply_segemnts.ack))
                        else:
                            f.write('snd    {:<.2f}   A    {:<d}  {:<d}  {:<d}\n'.format((time.time() - start),
                                                                                         reply_segemnts.seq,0,
                                                                                         reply_segemnts.ack))
                    lis.pop()
                    lis.append(ack)

                else:
                    count_duplicate += 1
                continue


            if received_segments.Fin:
                with open('Receiver_log.txt', 'a') as f:
                    f.write('rcv    {:<.2f}   F   {:<d}  {:<d}  {:<d}\n'.format((time.time() - start) ,
                                                                                  received_segments.seq, 0,
                                                                                  received_segments.ack))
                reply_segemnts = Segment(Fin=1,seq=server_isn,ack=received_segments.seq +1,ACK = 1)
                reply_segemnts = check_sum_send(reply_segemnts)
                s.sendto(pickle.dumps(reply_segemnts),address)
                with open('Receiver_log.txt', 'a') as f:
                    f.write('snd     {:<.2f}   A    {:<d}  {:<d} {:<d}\n'.format((time.time() - start) ,
                                                                                  reply_segemnts.seq, 0,
                                                                                  reply_segemnts.ack))
                    f.write('snd     {:<.2f}   F    {:<d}  {:<d} {:<d}\n'.format((time.time() - start),
                                                                                 reply_segemnts.seq, 0,
                                                                                 reply_segemnts.ack))
                while True:
                    data,address = s.recvfrom(2048)
                    if not data:
                        break
                    seg_num += 1
                    received_segments = pickle.loads(data)
                    with open('Receiver_log.txt', 'a') as f:
                        f.write('rcv    {:<.2f}   A    {:<d}  {:<d}  {:<d}\n'.format((time.time() - start),
                                                                                      received_segments.seq, 0,
                                                                                      received_segments.ack))
                    if received_segments.ACK and received_segments.ack == server_isn + 1:
                        break

                with open(output_file,'ab') as f1:
                    for key in sorted(seq_dict):
                        f1.write(seq_dict[key])

                with open('Receiver_log.txt', 'a') as f:
                    f.write('==============================================\n')
                    f.write('Amount of data received (bytes)      {}\n'.format(data_len))
                    f.write('Total Segments Received              {}\n'.format(seg_num))
                    f.write('Data segments received               {}\n'.format(data_contain))
                    f.write('Data segments with Bit Errors        {}\n'.format(error))
                    f.write('Duplicate data segments received     {}\n'.format(count_duplicate))
                    f.write('Duplicate ACKs sent                  {}\n'.format(dup_ack))
                    f.write('==============================================')
                break
        else:
            error += 1
            with open('Receiver_log.txt', 'a') as f:
                f.write('drop/corr     {:<.2f}   D   {:<d}  {:<d}  {:<d}\n'.format((time.time() - start) ,
                                                                                          received_segments.seq,
                                                                                          len(received_segments.data),
                                                                                          received_segments.ack))





if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('WARNING:Not enough input parameters')
        sys.exit()
    port = int(sys.argv[1])
    # file name
    output_file = sys.argv[2]
    server_isn = 0
    seg_num = 0
    drop_num = 0
    count_duplicate = 0
    error = 0
    dup_ack = 0
    lis = [0]
    with open('Receiver_log.txt', 'w') as f:
        f.write('')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', port))
    print('Listening on port {}...'.format(port))
    start = time.time()
    first_ack = handshake()
    transfer_state()
    s.close()
