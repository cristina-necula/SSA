import socket

class Client():
    def __init__(self):

        print 'Connecting to server...'

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', 23456))

    def start(self):

        print 'Start entering commands. Connection closes on exit command'

        self.user_input = raw_input()

        while self.user_input != 'exit':
            self.socket.send(self.user_input)
            data = self.socket.recv(1024)
            print data
            self.user_input = raw_input()

        self.socket.send(self.user_input)
        self.socket.close()

        print ('Connection closed')

client = Client()
client.start()