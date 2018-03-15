import socket, ssl

HOST, PORT = "gandalf.whalebayco.com", 503

def handle(conn):
    print("sucessfully connected")
    print("match host name:", ssl.match_hostname(conn.getpeercert(), HOST))
    print("cert:", str(conn.getpeercert()))
    while True:
        conn.write(input("enter a message to send to the server: ").encode())
        print("received:", conn.recv().decode())

def main():
    #  look into the sock stream thing
    sock = socket.socket(socket.AF_INET)
    # sock = socket.socket(socket.AF_INET)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='second_full.pem')
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    # context.check_hostname = False
    conn = context.wrap_socket(sock, server_hostname=HOST)
    print("trying to connect to host:", HOST)
    try:
        conn.connect((HOST, PORT))
        handle(conn)
    finally:
        print("closing connection\n")
        conn.close()

if __name__ == '__main__':
    main()