import socket
import threading
from termcolor import colored

class ChatBoxClient:
    def __init__(self, host: str, port: int, username: str) -> None:
        # SERVER TO CONNECT ATTRIBUTES
        self.host: str = str(host)
        self.port: int = int(port)

        # YOUR IDENTIFICATION
        self.username: str = str(username)
        self.stopThreads: bool = False


    def send_message(self) -> None:
        while True:
            if self.stopThreads:
                return

            else:
                # GETS INPUT
                try:
                    clientMessage: str = input("")

                except KeyboardInterrupt:
                    print(colored(f"[-] Keyboard Interruption..", "red"))
                    self.stopThreads: bool = True # STOPS THREADS
                    self.socketConnection.close()
                    return

                if clientMessage == "/exit" or clientMessage == "/logout":
                    print(colored("[!] Closing connection..", "yellow"))
                    self.stopThreads: bool = True # STOPS THREADS
                    self.socketConnection.close()
                    return

                else:
                    # SENDS MESSAGE
                    # -- ENCRYPTION FUNCTION COMES HERE --
                    self.socketConnection.send(clientMessage.encode('ascii'))


    def recv_message(self) -> None:
        while True:
            if self.stopThreads:
                return

            else:
                try:
                    clientsResponse: bytes = self.socketConnection.recv(1024)
                    if clientsResponse:
                        print(clientsResponse.decode('ascii'))

                except Exception as error:
                    # print(colored(f"[-] Recv message error.", "red"))
                    # print(colored(f"[-] {error}.", "red"))
                    self.socketConnection.close()
                    return


    def connect(self) -> None:
        #INITIATING SOCKET
        self.socketConnection: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # CONNECTING TO SERVER
        self.socketConnection.connect((self.host, self.port))
        # IF CONNECTED
        print(colored(f"[+] Connected to host {self.host}, port {self.port}", "green"))

        # CLIENT CONSOLE CHAT
        try:
            #SENDS USERNAME TO THE SERVER
            self.socketConnection.send(self.username.encode('ascii'))

            recvMessageThread: threading = threading.Thread(target=self.recv_message)
            recvMessageThread.start()
            sendMessageThread: threading = threading.Thread(target=self.send_message)
            sendMessageThread.start()

        except Exception as error:
            print(colored(f"[-] Connection error.", "red"))
            print(colored(f"[-] {error}.", "red"))
            self.socketConnection.close()
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


# Example usage:
if __name__ == "__main__":
    # DEFAULT VALUES
    host: str = str(socket.gethostbyname(socket.gethostname()))
    port: int = 8846
    username: str = str(socket.gethostname())

    # START CLIENT
    ChatBoxClient(host=host, port=port, username=username).client_console()