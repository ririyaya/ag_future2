import socket
import time
import threading
req=b"\x30\x30\x30\x30\x30\x30\x36\x34\x23\x61\x67\x61\x69\x6e\x5f\x66\x6c\x61\x67\x3d\x30\x23\x75\x73\x65\x72\x5f\x69\x64\x3d\x31\x31\x30\x31\x38\x31\x35\x34\x34\x35\x23\x75\x73\x65\x72\x5f\x6b\x65\x79\x3d\x33\x34\x39\x38\x38\x35\x32\x30\x32\x23\x75\x73\x65\x72\x5f\x74\x79\x70\x65\x3d\x32\x23"

class Client:
    def __init__(self,host,port):
        self.port = port
        self.host = host
        self.status = 0
        self.BUF_SIZE = 1024
    def connect(self):
        self.client = socket.socket()
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.client.connect((self.host, self.port))
    def send(self):
        client.startResv()
        while True:
            self.client.send()
            time.sleep(1)
    def resv(self):
        while True:
            data = self.client.recv(self.BUF_SIZE)
            text = data.decode()
            print(text)
    def startResv(self):
        t = threading.Thread(target=self.resv)
        t.start()


client = Client('58.250.197.67',17002)
client.connect()
client.send(req)
#client.startResv()