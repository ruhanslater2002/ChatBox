import socket
import json
import threading
from termcolor import colored

class ChatBoxServer:
    def __init__(self) -> None:
        print(colored("[+] STARTING SERVER.", "green"))

        #JSON CONFIG FILE LOADER
        self.configFile: str = "config.json"
        self.configFile: dict = self.config_loader()

        # SERVER SETTINGS FROM JSON CONFIG
        try:
            self.serverHost: str = str(self.configFile['connection']['host'])
            self.serverPort: int = int(self.configFile['connection']['port'])
        except Exception as error:
            print(colored(f"[-] Initialising error, {error}.", "red"))

        # CONNECTIONS AND THREADS
        self.clientsConnected: list = []
        self.username: list = []
        self.stopThreads: bool = False

        # STARTING AND INISIALISING SERVER
        self.serverSocket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start_server()


    def start_server(self) -> None:
        try:
            # STARTING CONNECTION
            self.serverSocket.bind((self.serverHost, self.serverPort))
            # CONNECTIONS ALLOWED
            self.serverSocket.listen()

            print(colored("[+] SERVER RUNNING.", "green"))

            # STARTS THE CONSOLE HANDLER WHEN SERVER STARTS
            consoleHandler: threading = threading.Thread(target=self.console_handler)
            consoleHandler.start()

            while True:
                if self.stopThreads:
                    return
                else:
                    # STOPS LISTEN FOR CONNECTIONS
                    clientConnection, clientAddress = self.serverSocket.accept()

                    # APPENDS CONNECTION TO LIST
                    username: str = clientConnection.recv(1024)
                    self.username.append(username.decode('ascii'))
                    self.clientsConnected.append(clientConnection)

                    # SENDS MESSAGE THAT CONNECTED TO CONSOLE
                    print(colored(f"[+] Connection from {username.decode('ascii')} -> {clientAddress}", "green"))

                    clientHandler: threading = threading.Thread(target=self.client_connection_handler,
                                                                args=(clientConnection,
                                                                      clientAddress,
                                                                      username.decode('ascii')))
                    clientHandler.start()

        except Exception as error:
            self.stop_server()
            return


    def stop_server(self) -> None:
        # CLOSE CONNECTION
        self.stopThreads: bool = True
        self.serverSocket.close()
        return


    def config_loader(self) -> None:
        try:
            with open(self.configFile, "r") as file:
                configFile: dict = json.loads(file.read())
                return configFile

        except Exception as Error:
            print(colored(f"[-] Config loader error, {error}.", "red"))


    def msg_handler(self, message: str, clientConnection=None) -> None:
        for client in self.clientsConnected:
            if client != clientConnection:
                client.send(message.encode('ascii'))


    def console_handler(self) -> None:
        try:
            while not self.stopThreads:
                consoleMessage: str = input("")
                consoleCommand: str = consoleMessage.split()

                if consoleCommand[0] == "/stop":
                    # CLOSE CONNECTION
                    print(colored(f"[!] Stopping server..", "yellow"))
                    self.stop_server()
                    return
                elif consoleCommand[0] == "/show":
                    print("")
                    print("| SERVER CONNECTION")
                    print("")
                    print(f'└─> Server Host -> {colored(self.serverHost, "green")}')
                    print(f'└─> Server Port -> {colored(self.serverPort, "green")}')
                    print("")
                    print(f'└─> Connected -> {colored(self.username, "green")}')
                    print("")
                else:
                    consoleMessage = colored("CONSOLE", "red") + ": " + consoleMessage
                    self.msg_handler(message=consoleMessage)

        except Exception as error:
            print(colored(f"[-] Console handler error, {error}.", "red"))
            self.stop_server()
            return


    def client_connection_handler(self, clientConnection: socket, clientAddress: socket, clientUsername: str) -> None:
        # SENDS MESSAGE THAT CONNECTED
        self.msg_handler(message=colored(f"[+] {clientUsername} {clientAddress} connected.", "green"))
        try:
            while not self.stopThreads:
                clientReceive: bytes = clientConnection.recv(1024)

                if clientReceive:
                    # DEBUGS CLIENT CHATS ON SERVETR
                    print("CONSOLE: " + colored(clientUsername, "light_blue") + " -> " + clientReceive.decode('ascii'))
                    clientMessage: str = colored(clientUsername, "light_blue") + " -> " + clientReceive.decode('ascii')
                    self.msg_handler(message=clientMessage, clientConnection=clientConnection)

        except Exception as error:
            # CLOSE CLIENT CONNECTION IF ERROR OCCURS
            self.client_disconnection_handler(clientConnection=clientConnection,
                                              clientAddress=clientAddress,
                                              clientUsername=clientUsername)
            return


    def client_disconnection_handler(self, clientConnection: socket, clientAddress: socket, clientUsername: str) -> None:
        # CLOSE CLIENT CONNECTION
        # REMOVES CLIENT FROM ACTIVE LISTS
        if clientConnection in self.clientsConnected:
            self.clientsConnected.remove(clientConnection)

        if clientUsername in self.username:
            self.username.remove(clientUsername)

        print(colored(f"[-] {clientUsername} {clientAddress} disconnected.", "red"))

        # SENDS FOR CLIENTS
        self.msg_handler(message=colored(f"[-] {clientUsername} {clientAddress} disconnected.", "red"))

        # CLOSES CLIENT CONNECTION TO THE SERVER
        clientConnection.close()
        return


if __name__ == '__main__':
    ChatBoxServer()


