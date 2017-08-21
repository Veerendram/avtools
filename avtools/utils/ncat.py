import socket


class Netcat(object):
    """ Python 'netcat like' module """

    def __init__(self, ip, port):
        """
        Creates a TCP socket based on the ip and port number provided
        by user
        """
        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def read(self, length=1024):
        """
        Read 1024 bytes off the socket
        """
        return self.socket.recv(length)

    def write(self, data):
        """
        Writes data to Socket created
        """
        self.socket.send(data)

    def close(self):
        """
        Closes socket connection
        """
        self.socket.getsockname()
        self.socket.close()

