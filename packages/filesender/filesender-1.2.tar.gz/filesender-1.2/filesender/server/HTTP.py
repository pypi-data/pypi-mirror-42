import SimpleHTTPServer
import SocketServer
import os

server = None


class RootedHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    base = None

    def translate_path(self, path):
        """
        Get the path to a file from the path given in the request
        :param path: the path given in the request
        :return: the path
        """
        if self.base is None:
            return SimpleHTTPServer.SimpleHTTPRequestHandler.translate_path(self, path)
        else:
            words = path.split('/')
            words = filter(None, words)
            path = self.base
            for word in words:
                drive, word = os.path.splitdrive(word)
                head, word = os.path.split(word)
                if word in (os.curdir, os.pardir):
                    continue
                path = os.path.join(path, word)
            return path


def run(port, directory=None):
    """
        Run the server
        :param port: the port of the server
        :param directory: the directory to share
        :return:
        """
    global server
    RootedHandler.base = directory
    SocketServer.TCPServer.allow_reuse_address = True
    server = SocketServer.TCPServer(("", port), RootedHandler)
    try:
        server.serve_forever()
    except:
        if server is not None:
            server.server_close()
