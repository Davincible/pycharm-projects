import socket, ssl
from _thread import *
import json
from jose import jwt
import time

HOST, PORT, CERT = '10.244.85.206', 503, 'ip_full.pem'
# HOST, PORT, CERT = 'legolas.whalebayco.com', 503, 'ip_full.pem'

responses = {"connection_established": {"header": {"Code": 210}, "body": {}}}

users = {"hank": "thetank"}

def handle(conn):
    print("connection established")
    print("host name:", str(conn.getpeername()), "peer cert:", str(conn.getpeercert()))
    send_response(responses['connection_established'], conn)

    while True:
        client_request = conn.recv().decode()
        process_request(client_request, conn)

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
        request = json.loads(request)

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
        print(":meth: process_request error: invalid request from client, cannot load json")
        exit(1)

def load_rsa_keys(pub="publickey.pub", priv="mykey.pem"):
    print("loading rsa keys")
    with open(pub, 'r') as pub_key_file:
        public_key = pub_key_file.read()

    with open(priv, 'r') as priv_key_file:
        private_key = priv_key_file.read()

    return public_key, """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----""".encode()

def create_token(credentials):
    print("generating token")
    public_key, private_key = load_rsa_keys()

    username = list(credentials.keys())[0]
    password = credentials[username]
    if username in users and password == users[username]:
        print("username correct")
        payload = {"aud": username, "iss": "WB server", "jti": 636345, "did": "test_client"}
        start = time.time()
        token = jwt.encode(payload, private_key, algorithm="ES384")
        print("{} | generated token: {}".format(time.time() - start, token))

        return token


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