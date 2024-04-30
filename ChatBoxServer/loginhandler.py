import json
import hashlib
from termcolor import colored

class LoginHandler:
    def __init__(self, *, jsonFilePath="credentials.json", username: str, password: str) -> None:
        self.jsonFilePath: str = jsonFilePath
        self.username: str = username
        self.password: str = hashlib.sha256(password.encode()).hexdigest()


    def register(self) -> bool:
        try:
            newCredentials: dict = {"username": self.username, "password": self.password}

            with open(self.jsonFilePath, "r") as file:
                data: json = json.loads(file.read())

            # LOOPS AND CHECKS IF THE newCredentials ARE IN THE DATABASE ALREADY
            for credential in data['credentials']:
                if newCredentials['username'] == credential['username']:
                    print(colored("[-] Credentials already excist in database.", "red"))
                    return False

            # APPEND NEW CREDENTIALS
            data['credentials'].append(newCredentials)

            # UPDATE JSON FILE WITH DATA
            with open(self.jsonFilePath, "w") as file:
                json.dump(data, file, indent=4)

            return True

        except Exception as error:
            print(colored(f"[-] Check error, {error}.", "red"))
            return False


    def deregister(self) -> bool:
        try:
            with open(self.jsonFilePath, "r") as file:
                data: json = json.loads(file.read())

            usernameFound: bool = False

            # LOOKS FOR USERNAME IF FOUND IT WILL REMOVE
            for credential in data['credentials']:
                if self.username == credential['username'] and self.password == credential['password']:
                    data['credentials'].remove(credential)
                    usernameFound: bool = True
                    break

            if usernameFound:
                # WRITE THE FILE
                with open(self.jsonFilePath, "w") as file:
                    json.dump(data, file, indent=4)

            else:
                print(colored(f"[-] Username: {self.username}, Password: {self.password} not registered.", "red"))
                return False

        except Exception as error:
            print(colored(f"[-] Check error, {error}.", "red"))
            return False


    def check(self) -> bool:
        try:
            # OPENS JSON FILE AS READ ONLY
            with open(self.jsonFilePath, "r") as file:
                data: json = json.loads(file.read())

            # CHECKS AND MATCHES TO EVERY CREDENTIAL
            for credential in data['credentials']:
                if self.username == credential['username'] and self.password == credential['password']:
                    print(colored("[+] Credentials matched!", "green"))
                    return True

            print(colored("[-] Credentials did not matched.", "red"))
            return False

        except Exception as error:
            print(colored(f"[-] Check error, {error}.", "red"))
            return False

