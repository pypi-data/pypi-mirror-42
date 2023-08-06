# standard library imports
import socket
import logging


# Setting up the logger to be used by this module
logger = logging.getLogger(__name__)


class PhantomSocket:
    """
    Objects of this class handle the control connection to a phantom camera.

    CHANGELOG

    Added 20.02.2019
    """

    DEFAULT_PORT = 7115

    def __init__(self, ip):
        """

        :param ip:
        """
        # At the moment there is no need for being able to pass a custom port, because the phantom always runs on the
        # same port (given by DEFAULT_PORT) anyways.
        self.port = self.DEFAULT_PORT
        self.ip = ip
        logger.debug('Created a new PhantomSocket object to IP %s on PORT %s', self.ip, self.port)

        # Creating the socket object to be used to connect to the phantom
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination = self.get_host_tuple()
        self.socket.connect(destination)

    def get_host_tuple(self):
        """
        Returns a tuple, whose first element is the string IP address to connect to and the second being the int PORT.
        This is exactly the kind of tuple, that has to be passed to the socket constructor.

        CHANGELOG

        Added 20.02.2019

        :return: Tuple(str, int)
        """
        return self.ip, self.port

    def close(self):
        """
        Safely closes the socket, which is connected to the phantom

        CHANGELOG

        Added 20.02.2019

        :return:
        """
        self.socket.close()
