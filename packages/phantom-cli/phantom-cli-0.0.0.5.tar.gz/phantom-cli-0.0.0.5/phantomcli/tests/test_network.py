# Standard library import
from unittest import TestCase

# Package import
from phantomcli.network import PhantomSocket


class PhantomSocketTestCase(TestCase):

    GOOGLE_IP = '8.8.8.8'
    LOCALHOST_IP = '127.0.0.1'


class TestPhantomSocketBasic(TestCase):

    GOOGLE_IP = '8.8.8.8'
    LOCALHOST_IP = '127.0.0.1'

    def test_true_is_true(self):
        self.assertTrue(True)

    def test_ping_working_to_localhost(self):
        # Setting up a phantom socket, that points to the localhost and executing a ping. This ensures that the ping
        # command is generally working, because localhost should be addressable no matter what the network config
        phantom_socket = PhantomSocket(self.LOCALHOST_IP)
        is_pingable = phantom_socket.ping()
        self.assertTrue(is_pingable)

    def test_ping_working_to_google_network_connection(self):
        # Setting to google server (because we can assume, that it is always up) This will test the connection to the
        # internet
        phantom_socket = PhantomSocket(self.GOOGLE_IP)
        is_pingable = phantom_socket.ping()
        self.assertTrue(is_pingable)

