import threading
import socket
import logging
from FactValidationService.AbstractJobRunner import AbstractJobRunner

class AssertionsRunner(AbstractJobRunner):

    def __init__(self, approach:str, port:int, assertions:list, result:list):
        super().__init__(approach, port)
        self.assertions = assertions
        self.result = result
        self.errorCount = 0
    
    def run(self):
        try:
            self.server = self._connect()
        except ConnectionRefusedError:
            return 
        
        result = self._execute()
        self.server.close()
        if result != None:
            self.result.extend(result)
            logging.info("Validated {} out of {} assertions successfully using {}."
                         .format(len(self.assertions) - self.errorCount, len(self.assertions), self.approach))

    def _execute(self):
        """
        Validate the assertions using self.approach.
        """
        result = []

        logging.info("Validating assertions using {}".format(self.approach))
        for assertion in self.assertions:
            response = self._validateAssertion(self.server, assertion)
            if type(response) == str and "ERROR" in response:
                self.errorCount += 1
                logging.warning("'{}' while validating {} using {}."
                                .format(response, assertion, self.approach))
            else:
                result.append((self.approach, assertion, response))
            
        return result