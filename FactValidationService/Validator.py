import logging

from FactValidationService.AssertionsRunner import AssertionsRunner
from FactValidationService.AssertionsCacheRunner import AssertionsCacheRunner
from FactValidationService.CacheRunner import CacheRunner

class Validator:
    def __init__(self, approaches, cachePath:str=None, useCache:bool=True):
        self.approaches = approaches
        self.cachePath = cachePath
        self.useCache = useCache

    def validate(self, assertions:list):
        """
        Validate the given assertions on every approach.
        Assertions expected as a list of triples [(s1, p1, o1), (s2, p2, o2), ...]
        Returns list of triples (approach, assertion, score)
        """
        result = []
        jobs = []
        
        # Start a thread for each approach
        for approach in self.approaches.keys():
            if self.useCache:
                jobRunner = AssertionsCacheRunner(approach, int(self.approaches[approach]), assertions, result, self.cachePath)
            else:
                jobRunner = AssertionsRunner(approach, int(self.approaches[approach]), assertions, result)
            jobs.append(jobRunner)
            jobRunner.start()
            
        # Wait for all threads to finish
        for job in jobs:
            job.join()

        return result
        
    def validateCache(self):
        jobs = []
        for approach in self.approaches.keys():
            jobRunner = CacheRunner(approach, int(self.approaches[approach]), self.cachePath)
            jobs.append(jobRunner)
            jobRunner.start()
            
        # Wait for all threads to finish
        for job in jobs:
            job.join()
            
        

