import socket
import json
import threading
import time
from termcolor import colored
import loginhandler

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
            self.serverSocket.listen()
            print(colored("[+] SERVER RUNNING.", "green"))
            # STARTS THE CONSOLE HANDLER WHEN SERVER STARTS
            consoleHandler: threading = threading.Thread(target=self.console_handler)
            consoleHandler.start()

            while not self.stopThreads:
                try:
                    # STOPS LISTEN FOR CONNECTIONS AND SENDS EACH CLIENT TO CLIENT HANDLER
                    clientConnection, clientAddress = self.serverSocket.accept()
                    print(colored(f"[+] Connection from {clientAddress}", "green"))
                    clientHandler: threading = threading.Thread(target=self.client_connection_handler, args=(clientConnection, clientAddress))
                    clientHandler.start()

                except Exception as error:
                    print(colored(f"[-] Disconnection from {clientAddress}", "red"))
                    clientConnection.close()

        except Exception as error:
            pass


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


    def client_connection_handler(self, clientConnection: socket, clientAddress: socket) -> None:
        while not self.stopThreads:
            clientConnection.send(colored("[!] (1) Login (2) Register", "yellow").encode('ascii'))
            clientOption: str = clientConnection.recv(1024).decode('ascii')
            time.sleep(0.1)

            if clientOption == "1":
                print(colored(f"[+] Client {clientAddress} selected option 1", "green"))
                # ASKS FOR USERNAME AND PASSWORD
                clientConnection.send(colored("[!] Username: ", "yellow").encode('ascii'))
                clientUsername: str = clientConnection.recv(1024).decode('ascii')
                time.sleep(0.1)
                clientConnection.send(colored("[!] Password: ", "yellow").encode('ascii'))
                clientPassword: str = clientConnection.recv(1024).decode('ascii')
                loginManage: loginhandler = loginhandler.LoginHandler(username=clientUsername, password=clientPassword)

                # CHECKS USERNAME AND PASSWORD
                if loginManage.check():
                    clientConnection.send(colored("[+] Successfully logged in.", "green").encode('ascii'))
                    # APPENDS CONNECTION TO LIST
                    self.username.append(clientUsername)
                    self.clientsConnected.append(clientConnection)

                    # SENDS MESSAGE THAT CONNECTED
                    self.msg_handler(message=colored(f"[+] {clientUsername} {clientAddress} connected.", "green"))

                    try:
                        while not self.stopThreads:
                            # WAITS FOR MESSAGE FROM CLIENT
                            clientReceive: bytes = clientConnection.recv(1024)
                            print("CONSOLE: " + colored(clientUsername, "light_blue") + " -> " + clientReceive.decode('ascii'))
                            clientMessage: str = colored(clientUsername, "light_blue") + " -> " + clientReceive.decode('ascii')
                            self.msg_handler(message=clientMessage, clientConnection=clientConnection)

                    except Exception as error:
                        # CLOSE CLIENT CONNECTION IF ERROR OCCURS
                        print(colored(f"[-] Disconnection from {clientAddress}", "red"))
                        self.client_disconnection_handler(clientConnection=clientConnection, clientAddress=clientAddress, clientUsername=clientUsername)
                        return

                else:
                    clientConnection.send(colored("[-] Login declined, password or username is incorrect.", "red").encode('ascii'))
                    print(colored(f"[-] Disconnection from {clientAddress}", "red"))
                    clientConnection.close()
                    return

            elif clientOption == "2":
                print(colored(f"[+] Client {clientAddress} selected option 2", "green"))
                # ASKS FOR USERNAME AND PASSWORD TO REGISTER
                clientConnection.send(colored("[!] New username: ", "yellow").encode('ascii'))
                clientNewUsername: str = clientConnection.recv(1024).decode('ascii')
                time.sleep(0.1)
                clientConnection.send(colored("[!] New password: ", "yellow").encode('ascii'))
                clientNewPassword: str = clientConnection.recv(1024).decode('ascii')
                # ADD USERNAME AND PASSWORD TO DATABASE
                loginManage: loginhandler = loginhandler.LoginHandler(username=clientNewUsername, password=clientNewPassword)
                loginManage.register()

            else:
                clientConnection.send(colored("[-] Unknown option.", "red").encode('ascii'))


    def client_disconnection_handler(self, *, clientConnection: socket, clientAddress: socket, clientUsername: str) -> None:
        # CLOSE CLIENT CONNECTION
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
