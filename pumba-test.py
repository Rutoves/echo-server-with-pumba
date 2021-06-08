import subprocess
import time
import logging

logging.basicConfig(format='[%(asctime)s | %(levelname)s]: %(message)s', datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.INFO)

def check_for_true():
    f = open('client/client.log', 'r')
    num_messages = int(f.read())
    f.close()

    f = open('client/client_message.txt', 'r')
    message = f.read()
    f.close()

    f = open('server/server.log')
    cur_number = 0
    for cur in f:
        cur = cur.strip()
        assert f'{cur_number} {message}' == cur, f"{cur_number} {message} not equal to {cur}"
        cur_number += 1
    f.close()
    logging.info('###SERVER WORKS CORRECTLY###')

while True:
    check_for_true()
    time.sleep(20)
