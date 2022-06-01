import threading
import socket
import logging

class AbstractJobRunner(threading.Thread):

    def __init__(self, approach:str, port:int):
        threading.Thread.__init__(self)
        self.approach = approach
        self.port = port
    
    def _validateAssertion(self, server, assertion):
        """
        Validate a single assertion.
        """
        return self._sendAssertion(server, assertion)
    
    def _connect(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect(("127.0.0.1", self.port))
            return server
        except ConnectionRefusedError as ex:
            logging.warning("Cannot connect to approach '{}'".format(self.approach))
            raise(ex)

    def _sendAssertion(self, server, assertion):
        request = "{} {} {}.".format(assertion[0], assertion[1], assertion[2])
        server.send(request.encode())
        return server.recv(1024).decode()