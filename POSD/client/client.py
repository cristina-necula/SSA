import socket

class Client():
    def __init__(self):

        print 'Connecting to server...'

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 23456))