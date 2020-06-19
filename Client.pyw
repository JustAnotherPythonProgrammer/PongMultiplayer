import socket

def once():
    from os import system
    system("cls")

once()
del once


class Client():

    def __init__(self, serverName, serverPort, sendPort, recvPort, timeout, backlog):
        self.SERVERNAME = serverName
        self.SENDPORT = sendPort
        self.RECVPORT = recvPort
        self.SERVERPORT = serverPort
        self.TIMEOUT = timeout
        self.BACKLOG = backlog
        self.HOST = socket.gethostname()

        self.player = None

        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sendSocket.bind((self.HOST, self.SENDPORT))
        print(f"Send socket bound on {self.HOST} to port {self.SENDPORT}.")

        self.recvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recvSocket.bind((self.HOST, self.RECVPORT))
        print(f"Recieve socket bound on {self.HOST} to port {self.RECVPORT}.")

        self.recvSocket.settimeout(self.TIMEOUT)
        print("Timeout: " + str(self.TIMEOUT))

        self.recvSocket.listen(self.BACKLOG)
        print("Backlog: " + str(self.BACKLOG))


    def connect(self):
        print("\n\n\nConnecting to server...\n")
        self.sendSocket.connect((self.SERVERNAME, self.SERVERPORT))
        self.sendSocket.send(self.HOST.encode() + b"|" + str(self.RECVPORT).encode())

        temp = self.recvSocket.accept()
        print(f"Send socket connected to server ({temp[1][0]}, {temp[1][1]}) using port {self.SENDPORT}.")
        print(f"Reciece socket connected to server ({temp[1][0]}, {temp[1][1]}) using port {self.RECVPORT}.")
        self.server = temp[0]
        temp = self.server.recv(32)
        self.player = int(temp.decode()) + 1
        print("\nPlayer: " + str(self.player))


    def send(self, data):
        self.sendSocket.send(data.encode())


    def recieve(self):
        return self.server.recv(32).decode()


    def close(self):
        self.sendSocket.close()
        self.recvSocket.close()
        print("\nClient closed.")
