import argparse
from pythonosc import udp_client, osc_message_builder

def establish_connection(host, port):
    server_ip = '127.0.0.1'
    server_port = '1666'
    client = udp_client.SimpleUDPClient(server_ip, server_port)

    while True:
        msg = input("what do you want to send to the server?")
        client.send_message()

