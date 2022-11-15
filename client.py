import socket
import threading

class Client:
    def __init__(self, DC_MSG, MAX_BYTES, FORMAT):
        self.DC_MSG = DC_MSG
        self.MAX_BYTES = MAX_BYTES
        self.FORMAT = FORMAT
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, SERVER, PORT):
        self.ADDR = (SERVER, PORT)
        self.client.connect(self.ADDR)

    def get_data(self):
        data = self.client.recv(self.MAX_BYTES)
        return data

    def send_message(self, msg):
        self.client.sendall(bytes(msg, self.FORMAT))

def handle_message(client):
    connected = True
    while connected:
        data = client.get_data()
        if not data:
            continue
        msg = data.decode(client.FORMAT)
        if msg.lower() == client.DC_MSG:
            break
        print(msg)

def main():
    client = Client(".env")
    client_thread = threading.Thread(target=handle_message, args=[client])
    client_thread.start()
    connected = True
    while connected:
        msg = input("msg:~ ")
        client.send_message(msg)
        if msg.lower() == client.DC_MSG:
            break
    client_thread.join()

if __name__ == "__main__":
    main()
