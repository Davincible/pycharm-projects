import socket, ssl
from _thread import *

# HOST, PORT, CERT = '10.244.85.206', 503, 'ip_full.pem'
HOST, PORT, CERT = 'legolas.whalebayco.com', 503, 'ip_full.pem'

def handle(conn):
    print("connection established")
    print("host name:", str(conn.getpeername()), "peer cert:", str(conn.getpeercert()))
    while True:
        print(conn.recv(10).decode())
        conn.write(b'this is a response from the server')

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
            start_new_thread(handle, (conn,))
        except ssl.SSLError as e:
            print(e)
        # finally:
        #     if conn:
        #         print("closing connection\n")
        #         conn.close()

if __name__ == '__main__':
    print("started the server")
    main()