import threading
import socket
import logging

class AbstractJobRunner(threading.Thread):

    def __init__(self, approach:str, port:int):
        threading.Thread.__init__(self)
        self.approach = approach
        self.port = port
        self.server = None
    
    def _validateAssertion(self, assertion):
        """
        Validate a single assertion.
        """
        return self._sendAssertion(assertion)
    
    def _connect(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect(("127.0.0.1", self.port))
        except ConnectionRefusedError as ex:
            logging.warning("Cannot connect to approach '{}'".format(self.approach))
            raise(ex)

    def _sendAssertion(self,  assertion):
        request = "{} {} {}.".format(assertion[0], assertion[1], assertion[2])
        if self.server == None:
            self._connect()
        self.server.send(request.encode())
        return self.server.recv(1024).decode()