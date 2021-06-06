from socket import *
import logging
import heapq
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('host', type=str, help='hostname to connect')
parser.add_argument('port', type=int, help='port to connect')
namespace = parser.parse_args()

host = namespace.host
port = namespace.port

logging.basicConfig(format='[%(asctime)s | %(levelname)s]: %(message)s', datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

addr = (host, port)

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(addr)

message_heap = []
cur_seq_num = 0

while True:
    logging.info('wait data...')

    conn, addr = sock.recvfrom(4096)
    if not conn:
        break

    try:
        data = bytes.decode(conn)
        seq_num = int(data[:data.find(' ')])
    except:
        logging.info('Message without info')
        sock.sendto(b'Hi', addr)
        continue

    heapq.heappush(message_heap, (seq_num, data))

    while message_heap and message_heap[0][0] == cur_seq_num:
        cur_message = heapq.heappop(message_heap)
        logging.info(f'Server received: {cur_message[1]}')
        sock.sendto(str.encode(cur_message[1]), addr)
        cur_seq_num += 1

sock.close()
