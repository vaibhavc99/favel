import logging

from FactValidationService.JobRunner import JobRunner as JobRunner

class Validator:
    def __init__(self, approaches, cachePath:str, useCache=True):
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
            jobRunner = JobRunner(approach, int(self.approaches[approach]), assertions, result, self.cachePath, self.useCache)
            jobs.append(jobRunner)
            jobRunner.start()
            
        # Wait for all threads to finish
        for job in jobs:
            job.join()

        return result
        

