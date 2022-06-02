import threading
import socket
import logging
from FactValidationService.Cache import Cache
from FactValidationService.AssertionsRunner import AssertionsRunner

class AssertionsCacheRunner(AssertionsRunner):

    def __init__(self, approach:str, port:int, assertions:list, result:list, cachePath:str):
        super().__init__(approach, port, assertions, result)
        threading.Thread.__init__(self)
        self.cachePath = cachePath
    
    def run(self):
        self.cache = Cache(self.cachePath, self.approach)
        super().run()
        self.cache.close()
            
    def _validateAssertion(self, assertion):
        result = self.cache.getScore(assertion[0], assertion[1], assertion[2])
        if result != None:
            return result
        
        result = super()._validateAssertion(assertion)
        if not "ERROR" in result:
            self.cache.insert(assertion[0], assertion[1], assertion[2], result)
        return result
        