import client

class StartClientFromCMD():
    def __init__(self):
        self.clientInstance = client.Client()

    def startClientFromCMD(self):
        print 'Start entering commands. Connection closes on exit command'
        self.user_input = raw_input()

        while self.user_input != 'exit':
            self.clientInstance.socket.send(self.user_input)
            data = self.clientInstance.socket.recv(1024)
            print data
            self.user_input = raw_input()

        self.clientInstance.socket.send(self.user_input)
        self.clientInstance.socket.close()

        print ('Connection closed')

client = StartClientFromCMD()
client.startClientFromCMD()