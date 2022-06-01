import threading
import socket
import logging
from FactValidationService.AbstractJobRunner import AbstractJobRunner

class CacheRunner(AbstractJobRunner):
    
    def __init__(self, approach:str, port:int, cachePath:str):
        super().__init__(approach, port)
        self.cachePath = cachePath
    
    def run(self):
        self.cache = Cache(self.cachePath, self.approach)
        super().run()
        self.cache.close()
        
    def _validateCache(self):
        cacheEntries = self.cache.getAll()
        for entry in cacheEntries:
            self._validateCacheEntry(entry)

    def _validateCacheEntry(self, assertion):
        validationResult = self._validateAssertion(assertion)
        if assertion[3] != validationResult:
            logging.info("Corrected {} cache".format(self.approach))
            self.cache.update(assertion[0], assertion[1], assertion[2], validationResult)