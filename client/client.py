from socket import *
import sys
import threading
import logging
import time
import argparse


def receive_message():
    while True:
        try:
            data = udp_socket.recv(4096)
        except Exception as e:
            logging.info(f'connection closed, {e}')
            udp_socket.close()
            sys.exit(1)

        if not data:
            udp_socket.close()
            sys.exit(1)

        data = bytes.decode(data)
        logging.info(f'client received "{data}"')

        if data in not_received_messages:
            not_received_messages.remove(data)


def send_again():
    while True:
        [udp_socket.sendto(str.encode(data), addr) for data in not_received_messages]
        time.sleep(2)


parser = argparse.ArgumentParser()
parser.add_argument('host', type=str, help='hostname to connect')
parser.add_argument('port', type=int, help='port to connect')
namespace = parser.parse_args()

host = namespace.host
port = namespace.port

logging.basicConfig(format='[%(asctime)s | %(levelname)s]: %(message)s', datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

addr = (host, port)

udp_socket = socket(AF_INET, SOCK_DGRAM)

logging.info('Waiting for server starting ...')
udp_socket.connect(addr)

while True:
    try:
        udp_socket.sendto(b'Hello', addr)
        udp_socket.recv(4096)
        break
    except:
        time.sleep(0.5)
        continue

logging.info('Client connected')

seq_num = 0

not_received_messages = set()

th1 = threading.Thread(target=receive_message)
th1.start()

th2 = threading.Thread(target=send_again)
th2.start()

with open('client_message.txt') as f:
    message = f.read()

with open('client.log', 'w') as log_file:
    while True:
        final_message = str(seq_num) + " " + message

        data = str.encode(final_message)

        udp_socket.sendto(data, addr)
        logging.info(f'client sended "{final_message}"')
        log_file.seek(0)
        log_file.write(str(seq_num))
        log_file.flush()

        not_received_messages.add(final_message)

        seq_num += 1
        time.sleep(5)
