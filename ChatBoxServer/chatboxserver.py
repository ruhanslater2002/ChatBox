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


    def client_handler(self, clientConnection: socket) -> None:
        try:
            while True:
                clientReceive: socket = clientConnection.recv(1024).decode()
                if clientReceive:
                    if clientReceive == "/exit":
                        return
                    else:
                        print(clientReceive)


        except Exception as error:
            # CLOSE CONNECTION
            print(colored(f"[-] Client handle error.", "red"))
            print(colored(f"[-] {error}.", "red"))
            self.serverStatus: str = colored("OFFLINE", "red")
            self.serverSocket.close()
            return


    def start_server(self) -> None:
        # STARTING CONNECTION
        self.serverSocket.bind((self.serverHost, self.serverPort))
        self.status: str = colored("RUNNING", "green")
        # CONNECTIONS ALLOWED
        self.serverSocket.listen(5)

        print(colored("[+] Server running..", "green"))
        try:
            while True:
                # ACCEPT CONNECTIONS
                clientConnection, clientAddress = self.serverSocket.accept()
                #APPENDS CONNECTION TO LIST
                self.clientsConnected.append(clientConnection)
                print(colored(f"[+] Connection from {clientConnection} -> {clientAddress}", "green"))

                clientHandler: threading = threading.Thread(target=self.client_handler, args=(clientConnection,))
                clientHandler.start()

        except Exception as error:
            # CLOSE CONNECTION
            print(colored(f"[-] Server error.", "red"))
            print(colored(f"[-] {error}.", "red"))
            self.serverStatus: str = colored("OFFLINE", "red")
            self.serverSocket.close()
            return


    def server_execute_command(self, command: str) -> None:
        # EXECUTE COMMANDS
        if command[0] == "show":
            print("")
            print("| SERVER CONNECTION")
            print(f'└─> Server Host (set serverhost <serverhost>) -> {colored(self.serverHost, "green")}')
            print(f'└─> Server Port (set serverport <serverport>) -> {colored(self.serverPort, "green")}')
            print("")
        elif command[0] == "start":
            # STARTS THE SERVER
            print(colored(f"[+] Starting connection on host {self.serverHost}, port {self.serverPort}", "green"))
            try:
                self.start_server()
            except Exception as error:
                self.serverStatus: str = colored("OFFLINE", "red")
                print(colored(f"[-] {error}.", "red"))


        # SETS VALUES
        elif command[0] == "set" and command[1] == "serverhost":
            try:
                self.serverHost: str = str(command[2])
                print(colored(f"[+] Server host has been set to {self.serverHost}", "green"))
            except Exception as error:
                print(colored(f"[-] {error}.", "red"))
        elif command[0] == "set" and command[1] == "serverport":
            try:
                self.serverPort: int = int(command[2])
                print(colored(f"[+] Server port has been set to {self.serverPort}", "green"))
            except Exception as error:
                print(colored(f"[-] {error}.", "red"))

        else:
            print(colored("[-] Unknown command!", "red"))


    def server_console(self) -> None:
        # SEVER CONSOLE
        while True:
            serverCommand: str = input(f"\n┌──({colored("SERVER", "green")})-({self.serverStatus}) \n└─> ")
            if serverCommand == 'exit' or serverCommand == 'stop':
                # STOPS SERVER
                print(colored("[!] Closing server..", "yellow"))
                return
            else:
                self.server_execute_command(command=serverCommand.split())


if __name__ == '__main__':
    # DEFAULT VALUES
    serverHost: str = "127.0.0.1"
    serverPort: int = 8846

    # START CLIENT
    print(colored("[+] Starting server..", "green"))
    ChatBoxServer(serverHost=serverHost, serverPort=serverPort).server_console()
    print(colored("[-] Server has stopped.", "red"))


