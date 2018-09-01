import socket
import time
from bitstring import BitStream, BitArray
import json

print("Client")
# host = '10.244.85.206'
# host = 'gandalf.whalebayco.com'
host = '127.0.0.1'
port = 501

data_dict = {"a": 1, "b": 2, "c": 3}
converted = json.dumps(data_dict)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((host, port))
except socket.error as e:
    print("An error occured:", e)
    exit(1)

message = 'This is a test message'
confirmation_message = s.recv(2048).decode('utf-8')
print(confirmation_message)
for i in range(5):
    message = input("Send a message to the server: ")
    if message == "json":
        print("Sending json")
        message = converted

    s.send(message.encode())
    data = s.recv(2048)
    print(data.decode())
    # time.sleep(2)



