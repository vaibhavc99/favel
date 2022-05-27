import threading
import socket
import logging
from FactValidationService.ValidatorCache import ValidatorCache

class JobRunner(threading.Thread):

    def __init__(self, approach:str, port:int, assertions:list, result:list, cachePath:str, useCache=True):
        threading.Thread.__init__(self)
        self.approach = approach
        self.port = port
        self.assertions = assertions
        self.result = result
        self.errorCount = 0
        self.useCache = useCache
        self.cachePath = cachePath
    
    def run(self):
        self.cache = ValidatorCache(self.cachePath)
        result = self._execute()
        if result != None:
            self.result.extend(result)
            logging.info("Validated {} out of {} assertions successfully using {}."
                         .format(len(self.assertions) - self.errorCount, len(self.assertions), self.approach))
        self.cache.close()

    def _execute(self):
        """
        Validate the assertions using approach.
        """
        try:
            client = self._connect()
            result = []

            logging.info("Validating assertions using {}".format(self.approach))
            for assertion in self.assertions:
                response = self._validateAssertion(client, assertion)
                if type(response) == str and "ERROR" in response:
                    self.errorCount += 1
                    logging.warning("'{}' while validating {} using {}."
                                    .format(response, assertion, self.approach))
                else:
                    result.append((self.approach, assertion, response))
            
            client.close()
            return result
        except ConnectionRefusedError:
            logging.warning("Cannot connect to approach '{}'".format(self.approach))
            
    def _validateAssertion(self, client, assertion):
        result = None
        if self.useCache:
            result = self.cache.getScore(self.approach, assertion[0], assertion[1], assertion[2])
            
        if result != None:
            return result
        
        result = self._sendAssertion(client, assertion)
            
        if self.useCache and (not "ERROR" in result):
            self.cache.insert(self.approach, assertion[0], assertion[1], assertion[2], result)
            
        return result
    
    def _connect(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", self.port))
        return client

    def _sendAssertion(self, client, assertion):
        request = "{} {} {}.".format(assertion[0], assertion[1], assertion[2])
        client.send(request.encode())
        return client.recv(1024).decode()