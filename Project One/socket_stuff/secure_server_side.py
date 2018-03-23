import socket, ssl
from _thread import *
import json
import time
import jwt

HOST, PORT, CERT = '10.244.85.206', 503, 'ip_full.pem'
# HOST, PORT, CERT = 'legolas.whalebayco.com', 503, 'ip_full.pem'

responses = {"connection_established": {"header": {"Code": 210}, "body": {}}}

users = {"hank": "thetank"}

def handle(conn):
    print("connection established")
    print("host name:", str(conn.getpeername()), "peer cert:", str(conn.getpeercert()))
    send_response(responses['connection_established'], conn)

    while True:
        client_request = conn.recv()

        if client_request.strip():
            process_request(client_request, conn)
        else:
            print("received empty request")

def send_response(response, conn):
    if isinstance(response, type(dict())):
        request = json.dumps(response)
    else:
        request = response

    # make sure the request is a string, no need for handling of there objects types than dicts, because it would be
    # an invalid request anyway
    assert(isinstance(request, type(str())))

    conn.send(request.encode())

def process_request(request, conn):
    print("calling the processing method")
    try:
        request = json.loads(request.decode())

        ## should do some validation shit
        function_call = request['header']['FunctionCall']
        print("the function call is:", function_call)
        if function_call == 'request_token':
            credentials = {request['body']['Data']['username']: request['body']['Data']['password']}
            print("calling token method")
            token = create_token(credentials)
            response = {'header': {'Code': 200, 'GoodResponse': True, 'FunctionCall': function_call}, 'body': {'Data': token}}
            send_response(response, conn)

    except ValueError:
        print(":meth: process_request error: invalid request from client, cannot load json\n    : ", request)
        exit(1)

def load_rsa_keys(pub="publickey.pub", priv="ec_key_01.pem"):
    print("loading rsa keys")
    with open(pub, 'r') as pub_key_file:
        public_key = pub_key_file.read()

    with open(priv, 'r') as priv_key_file:
        private_key = priv_key_file.read().encode()

    # cert_obj = load_pem_x509_certificate(private_key.encode(), default_backend())
    return public_key, private_key

def create_token(credentials):
    print("generating token")
    public_key, private_key = load_rsa_keys()

    username = list(credentials.keys())[0]
    password = credentials[username]
    if username in users and password == users[username]:
        print("username correct")
        payload = {"aud": username, "iss": "WB server", "jti": 636345, "did": "test_client"}
        start = time.time()
        token = jwt.encode(payload, private_key, algorithm="ES512")
        print("{} | generated token: {}".format(time.time() - start, token))

        return token.decode()


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