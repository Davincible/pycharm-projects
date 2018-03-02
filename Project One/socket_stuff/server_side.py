import socket
from _thread import *

host = ''
port = 501
buffer_size = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except socket.error as e:
    print("some error occured:", str(e))

s.listen(2)
print("Server started, waiting for connections.")

def client(conn):
    conn.send(str.encode("Connection to server established, u want sum ?\n"))

    while True:
        data = conn.recv(buffer_size)
        reply = "Message recieved: " + data.decode('utf-8')

        if not data:
            break

        conn.sendall(str.encode(reply))
    conn.close()

if __name__ == '__main__':
    while True:
        conn, addr = s.accept()
        print("Connected to: "+addr[0]+':'+addr[1] + '\n    full address:' + addr)

        start_new_thread(client, (conn,))