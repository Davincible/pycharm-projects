import socket
import time
from bitstring import BitStream, BitArray


# host = '10.244.85.206'
host = 'gandalf.whalebayco.com'
port = 501

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((host, port))
except socket.error as e:
    print("An error occured:", e)

message = 'This is a test message'
confirmation_message = s.recv(2048).decode('utf-8')
print(confirmation_message)
for i in range(5):
    s.send(message.encode())
    data = s.recv(2048)
    print("Recieved data:", data.decode())
    # time.sleep(2)
    message = input()


