import socket


class IP:
    def __init__(self):
        pass

    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        x = s.getsockname()
        return x[0]
