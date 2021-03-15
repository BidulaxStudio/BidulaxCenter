import socket

class BidulaxCenterClient:

    def __init__(self, host, port, buf_size):
        self.host = host
        self.port = port
        self.buf_size = buf_size

    def send(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as bc_client:
            bc_client.connect((self.host, self.port))
            print(f"[CLIENT] Connection to ('{self.host}', {self.port})")
            bc_client.sendall(bytes(data, "utf-8"))
            return str(bc_client.recv(self.buf_size), "utf-8")


client = BidulaxCenterClient("localhost", 25575, 1024)
while True:
    sentence = input(f"Enter a request for ({client.host}, {client.port}) :")
    if sentence == "CLIENT | STOP": break
    print(client.send(sentence))
