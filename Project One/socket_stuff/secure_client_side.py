import socket, ssl
import json

HOST, PORT = "10.244.85.206", 503

responses = {"invalid_json_string": {"header": {"Code": 401}, "body": {"Error_Description": "Error while loading string as json"}},
             "invalid_json_format": {"header": {"Code": 402}, "body": {"Error_Description": "invalid json format"}},
             "closing_connection": {"header": {"FunctionCall": "close_connection"}, "body": {}}}

def handle(conn):
    print("successfully connected")
    try:
        # listen for confirmation message from the server
        resp = conn.recv().decode()

        # convert response to json and check if valid
        resp = validate(resp, conn)
        process(resp, conn)

    except ValueError:
        conn.write(json.dumps(responses['invalid_json_string']).encode())

def validate(response, conn):
    valid_response = False
    counter = 0

    while not valid_response:
        response = json.loads(response)

        if counter > 5:
            print("error code 402 was encountered 5 times in a row")
            exit(402)

        # check if the received json is valid according to the protocol,
        # meaning the root keywords are 'header' and 'body'
        if response.keys() != {"header": None, "body": None}.keys():
            print("invalid response, error code 402")
            response = make_request(responses['invalid_json_format'], conn)
            counter += 1
        else:
            valid_response = True

    return response

def process(response, conn):
    response_code = response['header']['Code']

    if response_code is 200:
        # request has been processed correctly, return data
        return True, response
    elif response_code is 210:
        # connection with server established, respond with login credentials and ask for JWT
        authenticate(conn)

def make_request(request, conn):
    if isinstance(request, type(dict())):
        request = json.dumps(request)

    # make sure the request is a string, no need for handling of there objects types than dicts, because it would be
    # an invalid request anyway
    assert(isinstance(request, type(str())))

    conn.send(request.encode())
    response = conn.recv().decode()
    validate(response, conn)
    return response

def authenticate(conn, username="hank", password="thetank"):
    data = {"username": username, "password": password}
    request = {"header": {"FunctionCall": "request_token"}, "body": {"Data": data}}
    resp = validate(make_request(request, conn), conn)

    if not resp['header']['Code'] is 200:
        print("didn't receive code 200 while authenticating, exiting")
        exit(resp['header']['Code'])

    auth_token = resp['body']['Data']
    print("Collected auth token:", auth_token)

def main():
    #  look into the sock stream thing
    sock = socket.socket(socket.AF_INET)
    # sock = socket.socket(socket.AF_INET)
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='ip_full.pem')
    context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
    # context.check_hostname = False
    conn = context.wrap_socket(sock, server_hostname=HOST)
    print("trying to connect to host:", HOST)
    try:
        conn.connect((HOST, PORT))
        handle(conn)
    except ssl.SSLError as e:
        print("SSL Error: couldn't verify;", e)
        exit(1)
    finally:
        print("closing connection\n")
        make_request(responses['closing_connection'], conn)
        conn.close()

if __name__ == '__main__':
    main()