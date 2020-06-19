import socket
from sys import argv, exit
from time import sleep
from random import randint

def once():
    from os import system
    system("cls")

once()
del once



class Connection():
    def __init__(self, recv, name, ip, port, portToBind, timeout, player):
        self.recieveSocket = recv

        self.NAME = name
        self.IP = ip
        self.PORT = port
        self.PORTTOBIND = portToBind
        self.TIMEOUT = timeout


        self.recieveSocket.settimeout(self.TIMEOUT)

        self.sendSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sendSocket.bind((socket.gethostname(), self.PORTTOBIND))
        self.sendSocket.settimeout(timeout)
        self.sendSocket.connect((self.NAME, self.PORT))
        self.send(str(player))
        sleep(0.01)


    def send(self, data):
        self.sendSocket.send(data.encode())


    def recieve(self):
        return self.recieveSocket.recv(32).decode()


    def close(self):
        self.sendSocket.close()




class Server():
    def __init__(self, port, timeout, backlog):
        self.HOST = socket.gethostname()
        self.PORT = port
        self.TIMEOUT = timeout
        self.BACKLOG = backlog


        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER.bind((self.HOST, self.PORT))
        print(f"Server socket bound on {self.HOST} to port {self.PORT}.")

        self.SERVER.settimeout(self.TIMEOUT)
        print(f"Timeout: {self.TIMEOUT}")

        self.SERVER.listen(self.BACKLOG)
        print(f"Backlog: {self.BACKLOG}")
        print("Waiting for connections...\n\n\n")


    def findClients(self, timeout):
        self.connections = []
        for i in range(2):
            item = self.SERVER.accept()

            temp = item[0].recv(64).decode()
            name, port = temp.split("|")
            port = int(port)

            print(f"Connection from {name} ({item[1][0]}, {item[1][1]}) using port {self.PORT}.")
            self.connections.append(Connection(item[0], name, item[1][0], port, 8081 + i, timeout, i))


    def sendAll(self, data):
        for c in self.connections:
            c.send(data)


    def sendSpecific(self, index, data):
        self.connections[index].send(data)


    def recieve(self, index):
        return self.connections[index].recieve()


    def close(self):
        self.SERVER.close()
        for c in self.connections:
            c.close()
        print("Server closed.")




def main():
    try:
        server = Server(int(argv[1]), int(argv[2]), int(argv[3]))
    except IndexError:
        server = Server(8080, 30, 0)
    try:
        server.findClients(2)

        deltaX = 2
        deltaY = -1


        server.sendAll(f"195|195|{deltaX}|{deltaY}/120|120")
        sleep(1)

        while True:
            data = server.recieve(0)
            server.sendSpecific(1, data)

            data = server.recieve(1)
            server.sendSpecific(0, data)

    except socket.timeout:
        print("Player disconnected.")
        server.close()
        exit(0)

    except Exception as e:
        print(f"\n\nError: {e}\n")
        server.close()
        exit(0)


if __name__ == "__main__":
    main()
