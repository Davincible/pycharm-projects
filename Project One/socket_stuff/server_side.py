import socket
from _thread import *
print("Server")

# host = ''
host = '' #'gandalf.whalebayco.com'
port = 501
buffer_size = 2048

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.settimeout(0.0)

try:
    s.bind((host, port))
    print("socket name:", s.getsockname())
except socket.error as e:
    print("some error occured:", str(e))

s.listen(2)
print("Server started, waiting for connections.")

def client(conn):
    conn.send(str.encode("Connection to server established, Would you like to send a message?\n"))

    while True:
        # print("beginning of the while loop")
        data = conn.recv(buffer_size)
        print("received from client:", data)
        reply = "Message recieved: " + data.decode('utf-8') + '\n'

        if not data:
            print("calling break")
            break

        conn.send(reply.encode())
    print("closing connection")
    conn.close()

if __name__ == '__main__':
    while True:
        print("listening")
        conn, addr = s.accept()
        print("Connected to: "+addr[0]+':'+str(addr[1]) + '\n    full address:' + str(addr))

        start_new_thread(client, (conn,))