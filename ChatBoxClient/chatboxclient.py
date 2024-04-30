import socket
import threading
from termcolor import colored

class ChatBoxClient:
    def __init__(self) -> None:
        # SERVER TO CONNECT ATTRIBUTES
        self.host: str = "192.168.0.10"
        self.port: int = 8846
        self.username: str = "admin"
        self.password: str = "password123"
        self.stopThreads: bool = False
        self.client_console()


    def send_message_handler(self) -> None:
        while not self.stopThreads:
            # GETS INPUT
            try:
                clientMessage: str = input("")

            except KeyboardInterrupt:
                print(colored(f"[-] Keyboard Interruption..", "red"))
                self.close_connection()
                return

            if clientMessage == "/exit" or clientMessage == "/logout":
                print(colored("[!] Closing connection..", "yellow"))
                self.close_connection()
                return

            else:
                # SENDS MESSAGE
                # -- ENCRYPTION FUNCTION COMES HERE --
                try:
                    self.socketConnection.send(clientMessage.encode('ascii'))
                except Exception as error:
                    print(colored("[-] Connection lost.", "red"))
                    self.close_connection()


    def recv_message_handler(self) -> None:
        while not self.stopThreads:
            try:
                clientsResponse: bytes = self.socketConnection.recv(1024)
                if clientsResponse:
                    print(clientsResponse.decode('ascii'))

            except Exception as error:
                self.close_connection()
                return


    def connect(self) -> None:
        # CONNECTING TO SERVER
        self.socketConnection: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketConnection.connect((self.host, self.port))
        print(colored(f"[+] Connected to host {self.host}, port {self.port}", "green"))

        # CLIENT CONSOLE CHAT
        try:
            recvMessageThread: threading = threading.Thread(target=self.recv_message_handler)
            sendMessageThread: threading = threading.Thread(target=self.send_message_handler)
            recvMessageThread.start()
            sendMessageThread.start()

        except Exception as error:
            print(colored(f"[-] Connection error.", "red"))
            print(colored(f"[-] {error}.", "red"))
            self.close_connection()
            return


    def close_connection(self) -> None:
        self.stopThreads: bool = True
        self.socketConnection.close()
        print(colored("[-] Connection closed.", "red"))
        return


    def client_console(self) -> None:
        # CLIENT CONSOLE
        while True:
            clientCommand: str = input(f"\n┌──({colored(self.username, "green")}) \n└─> ")
            clientCommand = clientCommand.split()
            if clientCommand[0] == 'exit' or clientCommand[0] == 'stop':
                # STOPS CLIENT
                print(colored("[!] Closing client..", "yellow"))
                return

            # EXECUTE COMMANDS
            elif clientCommand[0] == "show":
                print("")
                print("| IDENTIFICATION")
                print(f'└─>Username (set username <username>) -> {colored(self.username, "green")}')
                print(f'└─>Password (set password <password>) -> {colored(self.password, "green")}')
                print("")
                print("| CONNECTION")
                print(f'└─> Host (set host <host>) -> {colored(self.host, "green")}')
                print(f'└─> Port (set port <port>) -> {colored(self.port, "green")}')
                print("")

            elif clientCommand[0] == "connect":
                print(colored(f"[+] Connecting to host {self.host}, port {self.port}", "green"))
                try:
                    self.connect()
                    return # BREAKS SO THAT IT DOESN'T CONTINUE WITH THE THREADS

                except Exception as error:
                    print(colored(f"[-] Connection error.", "red"))
                    print(colored(f"[-] {error}", "red"))

            # SET VALUES
            elif clientCommand[0] == "set" and clientCommand[1] == "username":
                try:
                    self.username: str = str(clientCommand[2])
                    print(colored(f"[+] Username has been set to {self.username}", "green"))

                except Exception as error:
                    print(colored(f"[-] {error}", "red"))

            elif clientCommand[0] == "set" and clientCommand[1] == "password":
                try:
                    self.password: str = str(clientCommand[2])
                    print(colored(f"[+] Password has been set to {self.password}", "green"))

                except Exception as error:
                    print(colored(f"[-] {error}", "red"))

            elif clientCommand[0] == "set" and clientCommand[1] == "host":
                try:
                    self.host: str = str(clientCommand[2])
                    print(colored(f"[+] Host has been set to {self.host}", "green"))

                except Exception as error:
                    print(colored(f"[-] {error}", "red"))

            elif clientCommand[0] == "set" and clientCommand[1] == "port":
                try:
                    self.port: int = int(clientCommand[2])
                    print(colored(f"[+] Port has been set to {self.port}", "green"))

                except Exception as error:
                    print(colored(f"[-] {error}", "red"))

            else:
                print(colored("[-] Unknown command!", "red"))


if __name__ == "__main__":
    # START CLIENT
    ChatBoxClient()
