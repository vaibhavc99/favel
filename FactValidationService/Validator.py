import socket
import logging

class Validator:
    def __init__(self, approaches):
        self.approaches = approaches

    def validate(self, assertions:list):
        """
        Validate the given assertions on every approach.
        Assertions expected as a list of triples [(s1, p1, o1), (s2, p2, o2), ...]
        Returns list of triples (approach, assertion, score)
        """
        result = []
        for approach in self.approaches.keys():
            approachResult = self._execute(approach, assertions)
            if approachResult != None:
                result.extend(approachResult)
            
        return result
        

    def _execute(self, approach:str, assertions):
        """
        Validate the assertions using approach.
        """
        try:
            client = self._connect(int(self.approaches[approach]))
            result = []

            for assertion in assertions:
                result.append((approach, assertion, self._sendAssertion(client, assertion)))
            
            client.close()
            return result
        except ConnectionRefusedError:
            logging.info("Cannot connect to approach '{}'".format(approach))

    def _connect(self, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", port))
        return client

    def _sendAssertion(self, client, assertion):
        request = "{} {} {}.".format(assertion[0], assertion[1], assertion[2])
        client.send(request.encode())
        return client.recv(1024).decode()
