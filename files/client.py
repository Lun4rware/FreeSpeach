"""
Client.py
"""

from os import system as run
import socket
import base64
import json
import time

ADDRESS = "127.0.0.1"
PORT = 8082

COMMAND_LINES = []


def print_line(cmd):
    """
    Prints Line
    """
    COMMAND_LINES.append(cmd)
    run('clear')
    for line in COMMAND_LINES:
        print(line)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ADDRESS, PORT))


def send(message: str) -> bool:
    """
    Send a message to the server
    """
    data = {
        'message': message,
        'time': str(time.time())
    }
    data['signiture'] = base64.b64encode((
        data['message'] + data['time']
    )
        .encode('utf-8')).decode('utf-8')
    data = json.dumps(data).encode('utf-8')
    data_length = str(len(data))
    data_length = data_length.encode('utf-8') + b' ' * (64 - len(data_length))
    client.send(data_length)
    client.send(data)
    recv_data_len = int(client.recv(64).decode('utf-8'))
    recv_data = client.recv(recv_data_len).decode('utf-8')
    print_line('SUCCESS' if json.loads(recv_data)
               ['status'] is '0' else 'FAILED')
    return True if '!DC' in message else False


run('clear')

while True:
    try:
        command = input('>> ')
        print_line(command)
        if send(command):
            break
    except KeyboardInterrupt:
        send('!DC')
        break
