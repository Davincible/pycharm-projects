import socket, ssl

HOST, PORT, CERT = 'gandalf.whalebayco.com', 503, 'second_full.pem'
# HOST, PORT, CERT = 'gandalf.whalebayco.com', 502, 'second_full.pem'

def handle(conn):
    print("connection established")
    print(conn.recv().decode())
    conn.write(b'this is a response from the server')
    print(str(conn.getpeername()), str(conn.getpeercert()))

def main():
    #  again look into sockstream
    # sock = socket.socket(socket.AF_INET)
    sock = socket.socket(socket.AF_INET)
    sock.bind((HOST, PORT))
    sock.listen(5)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
    print("socket created:", sock.getsockname())

    while True:
        print("waiting for connection")
        conn = None
        try:
            ssock, addr = sock.accept()
            conn = context.wrap_socket(ssock, server_side=True)
            handle(conn)
        except ssl.SSLError as e:
            print(e)
        finally:
            if conn:
                print("closing connection")
                conn.close()

if __name__ == '__main__':
    print("started the server")
    main()