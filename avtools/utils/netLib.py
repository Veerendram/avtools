import socket


class netLib(object):
    """Library containing miscellaneous tools to handle and check network interfaces
        and IP routing.
       As of version 0.1, this library contains keywords for:
       - Getting local host network interface IP address.
    """

    def __init__(self):
        return

    def get_local_IP(self):
        """Returns IP address of local host."""
        localIP = [(s.connect(('10.1.199.211', 53)), s.getsockname()[0],
                    s.close()) for s in [socket.socket(socket.AF_INET,
                    socket.SOCK_DGRAM)]][0][1]
        return localIP
