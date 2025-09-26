import socket

def mysocket(target):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return