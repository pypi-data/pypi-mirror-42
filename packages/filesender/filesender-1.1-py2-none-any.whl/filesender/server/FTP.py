from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

server = None


def run(port, directory=None):
    """
    Run the server
    :param port: the port of the server
    :param directory: the directory to share
    :return:
    """
    global server
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous(directory, perm="elradfmw")
    handler = FTPHandler
    if directory is not None:
        handler.authorizer = authorizer
    server = FTPServer(("", port), handler)
