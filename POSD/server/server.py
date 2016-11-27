import socket
import threading
import databaseAccessControl
import commandController

class MultithreadedServer(object):
    def __init__(self):
        self.initServer()
        self.running = True

    def initServer(self):
        print ('Initializing server ...')
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.bind(('127.0.0.1', 23456))

        self.initDatabase()
        self.commandController = commandController.CommandController()
        self.commandController.setDBAccessControl(self.dbAccessControl)

    def initDatabase(self):
        self.dbAccessControl = databaseAccessControl.DatabaseAccessControl()
        self.dbAccessControl.dropTables()
        self.dbAccessControl.createTables()
        self.dbAccessControl.addUserAndDefaultPermissions("bob", "bob")
        self.dbAccessControl.addUserAndDefaultPermissions("alice", "alice")
        self.dbAccessControl.addUserAndDefaultPermissions("root", "root")

    def start(self):
        self.listenForConnections()

    def listenForConnections(self):
        print ('Start listening for connections...')
        self.serverSocket.listen(5)
        while self.running:
            client, address = self.serverSocket.accept()
            print 'Connection started for ', address
            client.settimeout(10000)
            clientTread = threading.Thread(target=self.openConnectionForClient, args=(client, address))
            clientTread.start()

    def openConnectionForClient(self, client, address):
        currentThread = threading.currentThread()
        while getattr(currentThread, "do_run", True):
            clientCommand = client.recv(1024)
            if clientCommand:
                print 'Received from ', address, ' command ', clientCommand

                if clientCommand == 'exit':
                    self.closeConntectionForClient(client, address, currentThread)
                else:
                    response = self.commandController.parseAndExecute(str(clientCommand))
                    client.send(response)
        print 'Connection closed'

    def closeConntectionForClient(self, client, address, currentThread):
        print 'Client with address ', address, 'closed connection'
        print 'Stopping conection...'
        client.close()
        currentThread.do_run = False


server = MultithreadedServer()
server.start()