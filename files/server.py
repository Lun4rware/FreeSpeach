"""
Server File
"""

from base64 import b64encode
import threading
import socket
import json
import os
ADDRESS = "127.0.0.1"
PORT = 8082
ACTIVE_CLIENTS = []
COMMAND_LINES = []


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ADDRESS, PORT))
server.listen()


def print_line(cmd):
    """
    Prints Line
    """
    COMMAND_LINES.append(cmd)
    os.system('clear')
    for line in COMMAND_LINES:
        print(line)


def test_if_ok(message: str, time: str, message_hash: bytes) -> bool:
    """
    Tests if message and time match bytes
    """
    print(b64encode((message + time).encode('utf-8')))
    print(message_hash)
    return True if b64encode((message + time).encode('utf-8')) == message_hash else False


def handle_client(connection, address) -> None:
    """
    Handels Client Connections
    """
    connected = True
    while connected:
        data_length = int(connection.recv(64).decode('utf-8'))
        data = json.loads(connection.recv(data_length).decode('utf-8'))
        print_line(f'[{address[0]}] -> {data}')
        if data['message'] == '!DC':
            connected = False
        send_data = {
            # 0 == Okay
            # 1 == Error
            "status": "0" if test_if_ok(data['message'], data['time'], data['signiture'].encode('utf-8')) else "1",
            "message": data['message']
        }
        send_data = json.dumps(send_data).encode('utf-8')
        connection.send(str(len(send_data)).encode('utf-8') +
                        b' '*(64 - len(str(len(send_data)))))
        connection.send(send_data)


def start():
    """
    Start Listening
    """
    listening = True
    while listening:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            ACTIVE_CLIENTS.append(conn)
        except KeyboardInterrupt:
            listening = False


def test():
    """
    Test Command
    """
    print_line('Test Command')
    return False


def list_connections():
    """
    List All Connections
    """
    print_line(ACTIVE_CLIENTS)
    return False


def close_all_connections():
    """
    Close All Connections
    """
    for client in ACTIVE_CLIENTS:
        client.close()
        print_line(client)
    print_line('Closed All Connections!\n Press CTRL-C to exit!')
    return True


def help_thing():
    """
    help command
    """
    print_line("Help, test, stop, list (lists connections)")


def cmds():
    """
    Get Commands For Server
    """
    listening = True
    commands = {
        "help": help_thing,
        "test": test,
        "stop": close_all_connections,
        "list": list_connections
    }
    while listening:
        try:
            command = input('>> ').lower()
            cmd = commands[command] if command in commands else 'Invalid Command'
            if isinstance(cmd, str):
                print_line(cmd)
                continue
            if cmd():
                listening = False
        except KeyboardInterrupt:
            break


t1 = threading.Thread(target=start)
t2 = threading.Thread(target=cmds)
t1.start()
t2.start()
