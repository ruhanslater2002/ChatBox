import socket

from termcolor import colored

class ChatBoxClient:
    def __init__(self, host: str, port: int, username: str) -> None:
        # SERVER TO CONNECT ATTRIBUTES
        self.host: str = str(host)
        self.port: int = int(port)
        self.status: str = colored("OFFLINE", "red")

        # YOUR IDENTIFICATION
        self.username: str = str(username)


    def send_message(self) -> None:
        while True:

            # GETS INPUT
            try:
                clientMessage: str = input(f"{colored(self.username, "green")} -> ")
            except KeyboardInterrupt:
                print(colored(f"[-] Keyboard Interruption..", "red"))
                self.status: str = colored("OFFLINE", "red")
                self.socketConnection.close()
                return

            if clientMessage == "/exit" or clientMessage == "/logout":
                print(colored("[!] Closing connection..", "yellow"))
                self.socketConnection.close()
                self.status: str = colored("OFFLINE", "red")
                return

            else:
                # SENDS MESSAGE
                clientMessage: str = colored(self.username, "light_blue") + " -> " + clientMessage
                self.socketConnection.sendall(clientMessage.encode())  # MAKE ANOTHER FUNCTION THAT WILL ENCRYPT MESSAGE AND RETURN
                self.recv_message()


    def recv_message(self) -> None:
        while True:
            clientsResponse: socket = self.socketConnection.recv(1024).decode()
            if clientsResponse:
                print(clientsResponse)
                return


    def connect(self) -> None:
        # RESETS INSTANCE
        self.socketConnection: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # CONNECTING TO SERVER
        self.socketConnection.connect((self.host, self.port))
        print(colored(f"[+] Connected to host {self.host}, port {self.port}", "green"))
        self.status: str = colored("ONLINE", "green")

        # CLIENT CONSOLE CHAT
        try:
            self.send_message()

        except Exception as error:
            print(colored(f"[-] {error}", "red"))
            self.status: str = colored("OFFLINE", "red")
            self.socketConnection.close()
            return


    def client_execute_command(self, command: str) -> None:
        # EXECUTE COMMANDS
        if command[0] == "show":
            print("")
            print("| IDENTIFICATION")
            print(f'└─>Username (set username <username>) -> {colored(self.username, "green")}')
            print("")
            print("| CONNECTION")
            print(f'└─> Host (set host <host>) -> {colored(self.host, "green")}')
            print(f'└─> Port (set port <port>) -> {colored(self.port, "green")}')
            print("")
        elif command[0] == "connect":
            print(colored(f"[+] Connecting to host {self.host}, port {self.port}", "green"))
            try:
                self.connect()
            except Exception as error:
                self.status: str = colored("OFFLINE", "red")
                print(colored(f"[-] {error}", "red"))

        # SET VALUES
        elif command[0] == "set" and command[1] == "username":
            try:
                self.username: str = str(command[2])
                print(colored(f"[+] Username has been set to {self.username}", "green"))
            except Exception as error:
                print(colored(f"[-] {error}", "red"))
        elif command[0] == "set" and command[1] == "host":
            try:
                self.host: str = str(command[2])
                print(colored(f"[+] Host has been set to {self.host}", "green"))
            except Exception as error:
                print(colored(f"[-] {error}", "red"))
        elif command[0] == "set" and command[1] == "port":
            try:
                self.port: int = int(command[2])
                print(colored(f"[+] Port has been set to {self.port}", "green"))
            except Exception as error:
                print(colored(f"[-] {error}", "red"))

        else:
            print(colored("[-] Unknown command!", "red"))

    def client_console(self) -> None:
        # CLIENT CONSOLE
        while True:
            clientCommand: str = input(f"\n┌──({colored(self.username, "green")})-({self.status}) \n└─> ")
            if clientCommand == 'exit' or clientCommand == 'stop':
                # STOPS CLIENT
                print(colored("[!] Closing client..", "yellow"))
                return
            else:
                self.client_execute_command(command=clientCommand.split())


if __name__ == '__main__':
    # DEFAULT VALUES
    host: str = "127.0.0.1"
    port: int = 8846
    username: str = "ruhanslater2002"

    #START CLIENT
    ChatBoxClient(host=host, port=port, username=username).client_console()
    print(colored("[-] Client has stopped.", "red"))



