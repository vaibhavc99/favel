import socket
import logging

class Validation:
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
            result.extend(self._execute(approach, assertions))
            
        return result
        

    def _execute(self, approach:str, assertions):
        """
        Validate the assertions using approach.
        """
        client = self._connect(self.approaches[approach])
        result = []

        for assertion in assertions:
            result.append((approach, assertion, self._sendAssertion(client, assertion)))
            
        client.close()
        return result

    def _connect(self, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", port))
        return client

    def _sendAssertion(self, client, assertion):
        request = "{} {} {}.".format(assertion[0], assertion[1], assertion[2])
        client.send(request.encode())
        return client.recv(1024).decode()

approaches = dict()
approaches['knowledgestream'] = 4444
test = Validation(approaches)
print(test.validate([("<http://dbpedia.org/resource/Al_Attles>", "<http://dbpedia.org/ontology/team>", "<http://dbpedia.org/resource/Golden_State_Warriors>")]))
