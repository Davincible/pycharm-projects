import socket, ssl

HOST, PORT = "gandalf.whalebayco.com", 502

def handle(conn):
    print("sucessfully connected")
    conn.write(b'a message from a client\n')
    print("received:", conn.recv().decode())

def main():
    #  look into the sock stream thing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock = socket.socket(socket.AF_INET)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='cert.pem')
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    conn = context.wrap_socket(sock, server_hostname=HOST)
    print("trying to connect to host:", HOST)
    try:
        conn.connect((HOST, PORT))
        handle(conn)
    finally:
        conn.close()

if __name__ == '__main__':
    main()