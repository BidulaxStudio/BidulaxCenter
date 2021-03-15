from socket import socket, AF_INET, SOCK_STREAM
from database.database import BidulaxCenterDataBase
from datetime import datetime


class BidulaxCenterServer:

    def __init__(self, host, port, buf_size):

        print(f"--------------- {str(datetime.now())[:16]} ---------------")

        print("[SERVER] Setting up data...")

        self.database = BidulaxCenterDataBase()
        self.host = host
        self.port = port
        self.buf_size = buf_size

        try:
            open("SERVER", "r").close()
        except IOError:
            open("SERVER", "w").close()
            print("[SERVER] Fist start, setting up new user...")
            username = input("[SERVER] Enter an username :")
            password = input("[SERVER] Enter a password :")
            self.database.add_user(username, password)
            self.database.add_permission(username, "admin")
            print("[SERVER] User created. Please note that this is currently the only user of the server.")
            print("[SERVER] Please also note that this user has all the permissions on your server.")

        self.running = True
        self.socket = None
        self.connection = None
        self.address = None

        print("[SERVER] Starting server...")

        self.start()

    def start(self):
        with socket(AF_INET, SOCK_STREAM) as self.socket:
            self.socket.bind((self.host, self.port))
            self.socket.listen()
            while self.running:
                self.connection, self.address = self.socket.accept()
                with self.connection:
                    print(f'[SERVER] Connection from {self.address}')
                    while True:
                        data = self.connection.recv(self.buf_size)
                        if not data:
                            break
                        self.process(data.decode().split(" | "))

    def restart(self):
        print("[SERVER] The server will restart")
        with open(file="restart.py", mode="r") as restart:
            self.stop()
            exec(restart.read())

    def stop(self):
        print("[SERVER] Stopping...")
        self.running = False
        self.socket.close()
        self.database.close()
        print(f"--------------- {str(datetime.now())[:16]} ---------------")
        exit()

    def process(self, request):

        if len(request) < 3:
            self.connection.sendall("BAD REQUEST")
            return False

        username, password, action, *args = request

        if not self.database.user_exists(username, password):
            self.connection.sendall("NO CONNECTED")
            return False

        elif action == "SERVER":

            if args[0] == "RESTART":
                if self.database.has_permission(username, "server.restart"):
                    self.connection.sendall("SUCCESS".encode())
                    self.restart()
                else:
                    self.connection.sendall("NO PERMISSION".encode())

            elif args[0] == "STOP":
                if self.database.has_permission(username, "server.stop"):
                    self.connection.sendall("SUCCESS".encode())
                    self.stop()
                else:
                    self.connection.sendall("NO PERMISSION".encode())

            elif args[0] == "BACKUP":
                if self.database.has_permission(username, "server.backup"):
                    self.connection.sendall("SUCCESS".encode())
                    self.database.backup()
                else:
                    self.connection.sendall("NO PERMISSION".encode())

        elif action == "USER":

            if args[0] == "EXISTS":
                if self.database.has_permission(username, "user.exists"):
                    self.connection.sendall(("FALSE", "TRUE")[self.database.user_exists(args[1])].encode())
                else:
                    self.connection.sendall("NO PERMISSION".encode())

            elif args[0] == "ADD":
                if self.database.has_permission(username, "user.create"):
                    self.database.add_user(args[1], args[2])
                    self.connection.sendall("SUCCESS".encode())
                else:
                    self.connection.sendall("NO PERMISSION".encode())

            elif args[0] == "REMOVE":
                if self.database.has_permission(username, "user.remove"):
                    self.database.remove_user(args[1])
                    self.connection.sendall("SUCCESS".encode())
                else:
                    self.connection.sendall("NO PERMISSION".encode())

        elif action == "PERMISSION":

            if args[0] == "GET":

                if args[1] == "USERS":
                    if self.database.has_permission(username, "permission.get.users"):
                        users = ""
                        for user in self.database.get_users_who_have_permission(args[2]):
                            users += f" | {user}"
                        self.connection.sendall(users[3:].encode())
                    else:
                        self.connection.sendall("NO PERMISSION".encode())

                elif args[1] == "PERMISSIONS":
                    if self.database.has_permission(username, "user.get.permissions"):
                        permissions = ""
                        for permission in self.database.get_permissions_of_user(args[2]):
                            permissions += f" | {permission}"
                        self.connection.sendall(permissions[3:].encode())
                    else:
                        self.connection.sendall("NO PERMISSION".encode())

            elif args[0] == "ADD":

                if self.database.has_permission(username, "permission.add"):
                    self.database.add_permission(args[1], args[2])
                    self.connection.sendall("SUCCESS".encode())
                else:
                    self.connection.sendall("NO PERMISSION".encode())

            elif args[0] == "REMOVE":
                if self.database.has_permission(username, "permission.remove"):
                    self.database.remove_permission(args[1], args[2])
                    self.connection.sendall("SUCCESS".encode())
                else:
                    self.connection.sendall("NO PERMISSION".encode())

        elif action == "DATA":

            if args[0] == "GET":
                if self.database.has_permission(username, "data.get"):
                    self.connection.sendall(self.database.get_information(args[1]))
                else:
                    self.connection.sendall("NO PERMISSION".encode())

            elif args[0] == "ADD":
                if self.database.has_permission(username, "data.add"):
                    self.database.add_information(args[1], args[2])
                    self.connection.sendall("SUCCESS".encode())
                else:
                    self.connection.sendall("NO PERMISSION".encode())

            elif args[0] == "REMOVE":
                if self.database.has_permission(username, "data.remove"):
                    self.database.remove_information(args[1])
                    self.connection.sendall("SUCCESS".encode())
                else:
                    self.connection.sendall("NO PERMISSION".encode())

        self.connection.sendall("ENDED".encode())

BidulaxCenterServer("0.0.0.0", 25575, 1024)
