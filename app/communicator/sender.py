import threading
from socket import *

from app import node
from app.communicator import my_ip_address


def send(ip_address, message, port, *args):
    receiver_addr = (ip_address, port)
    tcp_socket = socket(AF_INET, SOCK_STREAM)
    try:
        tcp_socket.connect(receiver_addr)
        tcp_socket.send(message.encode('utf-8'))
    except Exception as e:
        print("Connection Failed while sending", e)


def send_to_all_node(message, except_my_node=False):
    address_list = list(map(lambda x: x.ip_address, node.get_all()))

    if except_my_node:
        address_list = list(filter(lambda x: x != my_ip_address.get_ip_address('en0'), address_list))

    send_threads = []

    for addr in address_list:
        try:
            t = threading.Thread(target=send, kwargs={'ip_address': addr,
                                                      'message': message,
                                                      'port': 3000})
            t.start()
            send_threads.append(t)
        except Exception as e:
            print("SENDTOALL EXCEPT", e)

    for thread in send_threads:
        thread.join()
