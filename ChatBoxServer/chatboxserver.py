import socket
import threading
from termcolor import colored

class ChatBoxServer:
    def __init__(self, serverHost: str, serverPort: int) -> None:
        # SERVER IDENTIFICATION ATTRIBUTES
        self.serverHost: str = serverHost
        self.serverPort: int = serverPort
        self.serverStatus: str = colored("OFFLINE", "red")

        # INITIATING INSTANCE
        self.serverSocket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsConnected: list = []
        self.username: list = []
        self.stopThreads: bool = False


    def msg_handler(self, message: str) -> None:
        for client in self.clientsConnected:
            client.send(message.encode('ascii'))


    def console_handler(self) -> None:
        while True:
            if self.stopThreads:
                return

            else:
                try:
                    consoleMessage: str = input("")
                    consoleCommand: str = consoleMessage.split()

                    if consoleCommand[0] == "stop":
                        print(colored(f"[!] Stopping server..", "yellow"))
                        self.stopThreads: bool = True
                        self.serverSocket.close()
                        return

                    else:
                        self.msg_handler(message=consoleMessage)


                except Exception as error:
                    # CLOSE CONNECTION
                    print(colored(f"[-] Console handler error, {error}.", "red"))
                    self.serverStatus: str = colored("OFFLINE", "red")
                    self.serverSocket.close()
                    return


    # RUNS IN THREADS
    def client_handler(self, clientConnection: socket, clientAddress: socket, username: socket) -> None:
        while True:
            if self.stopThreads:
                return

            else:
                try:
                    clientReceive: bytes = clientConnection.recv(1024)

                    if clientReceive:
                        #DEBUGS CLIENT CHATS ON SERVETR
                        print("CONSOLE: " + colored(username, "light_blue") + " -> " + clientReceive.decode('ascii'))

                        clientMessage: str = colored(username, "light_blue") + " -> " + clientReceive.decode('ascii')
                        self.msg_handler(message=clientMessage)

                except Exception as error:
                    # CLOSE CONNECTION
                    print(colored(f"[-] Client handle error, {error}.", "red"))

                    # REMOVES CLIENT FROM ACTIVE LISTS
                    if clientConnection in self.clientsConnected:
                        self.clientsConnected.remove(clientConnection)

                    if username in self.username:
                        self.username.remove(username)

                    print(colored(f"[-] {username} {clientAddress} disconnected.", "red"))
                    # SENDS FOR CLIENTS
                    self.msg_handler(message=colored(f"[-] {username} {clientAddress} disconnected.", "red"))

                    # CLOSES CLIENT CONNECTION TO THE SERVER
                    clientConnection.close()
                    return


    def start_server(self) -> None:
        # STARTING CONNECTION
        self.serverSocket.bind((self.serverHost, self.serverPort))
        self.status: str = colored("RUNNING", "green")
        # CONNECTIONS ALLOWED
        self.serverSocket.listen()

        print(colored("[+] Server running..", "green"))
        while True:
            if self.stopThreads:
                return

            else:
                try:
                    # STARTS THE CONSOLE HANDLER WHEN SERVER STARTS
                    consoleHandler: threading = threading.Thread(target=self.console_handler)
                    consoleHandler.start()
                    # ACCEPT CONNECTIONS

                    try:
                        clientConnection, clientAddress = self.serverSocket.accept() # ERROR WHEN STOP

                        # APPENDS CONNECTION TO LIST
                        username: str = clientConnection.recv(1024)

                        self.username.append(username.decode('ascii'))
                        self.clientsConnected.append(clientConnection)
                        # SENDS MESSAGE THAT CONNECTED TO CONSOLE
                        print(colored(f"[+] Connection from {username.decode('ascii')} -> {clientAddress}", "green"))
                        # SENDS MESSAGE THAT CONNECTED
                        self.msg_handler(message=colored(f"[+] {username.decode('ascii')} {clientAddress} connected.", "green"))

                        clientHandler: threading = threading.Thread(target=self.client_handler, args=(clientConnection,
                                                                                                      clientAddress,
                                                                                                      username.decode(
                                                                                                          'ascii')))
                        clientHandler.start()
                    except:
                        pass

                except Exception as error:
                    # CLOSE CONNECTION
                    print(colored(f"[-] Server error, {error}.", "red"))
                    self.serverStatus: str = colored("OFFLINE", "red")
                    self.serverSocket.close()
                    return


    def server_console(self) -> None:
        # SEVER CONSOLE
        while True:
            serverCommand: str = input(f"\n┌──({colored("SERVER", "green")})-({self.serverStatus}) \n└─> ")
            serverCommand: str = serverCommand.split()

            if serverCommand[0] == 'exit' or serverCommand[0] == 'stop':
                # STOPS SERVER
                print(colored("[!] Closing server config console..", "yellow"))
                return
            else:
                # EXECUTE COMMANDS
                if serverCommand[0] == "show":
                    print("")
                    print("| SERVER CONNECTION")
                    print(f'└─> Server Host (set serverhost <serverhost>) -> {colored(self.serverHost, "green")}')
                    print(f'└─> Server Port (set serverport <serverport>) -> {colored(self.serverPort, "green")}')
                    print("")
                elif serverCommand[0] == "start":
                    # STARTS THE SERVER
                    print(colored(f"[+] Starting connection on host {self.serverHost}, port {self.serverPort}", "green"))
                    try:
                        self.start_server()
                        return # BREAKS WHILE LOOP WHEN THREADING
                    except Exception as error:
                        self.serverStatus: str = colored("OFFLINE", "red")
                        print(colored(f"[-] {error}.", "red"))


                # SETS VALUES
                elif serverCommand[0] == "set" and serverCommand[1] == "serverhost":
                    try:
                        self.serverHost: str = str(serverCommand[2])
                        print(colored(f"[+] Server host has been set to {self.serverHost}", "green"))
                    except Exception as error:
                        print(colored(f"[-] {error}.", "red"))
                elif serverCommand[0] == "set" and serverCommand[1] == "serverport":
                    try:
                        self.serverPort: int = int(serverCommand[2])
                        print(colored(f"[+] Server port has been set to {self.serverPort}", "green"))
                    except Exception as error:
                        print(colored(f"[-] {error}.", "red"))

                else:
                    print(colored("[-] Unknown command!", "red"))


if __name__ == '__main__':
    # DEFAULT VALUES
    serverHost: str = "127.0.0.1"
    serverPort: int = 8846

    # START CLIENT
    print(colored("[+] Starting server..", "green"))
    ChatBoxServer(serverHost=serverHost, serverPort=serverPort).server_console()
    print(colored("[-] Server has stopped.", "red"))


