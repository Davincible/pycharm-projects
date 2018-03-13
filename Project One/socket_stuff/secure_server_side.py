import socket, ssl

HOST, PORT, CERT = '10.244.85.206', 502, 'cert.pem'

def handle(conn):
    print("connection established")
    print(conn.recv())
    conn.write(b'this is a response from the server', str(conn.getpeername()), str(conn.getpeercert()))

def main():
    #  again look into sockstream
    # sock = socket.socket(socket.AF_INET)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)
    context = ssl.create_default_context()
    context.load_cert_chain(certfile=CERT)
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
    print("socket created")

    while True:
        print("waiting for connection")
        conn = None
        ssock, addr = sock.accept()
        try:
            conn = context.wrap_socket(ssock, server_side=True)
            handle(conn)
        except ssl.SSLError as e:
            print(e)
        finally:
            if conn:
                conn.close()

if __name__ == '__main__':
    print("started the server")
    main()