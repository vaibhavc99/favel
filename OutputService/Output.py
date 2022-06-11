import pandas as pd
import csv

class Output:
        
    def getCleanOutput(self):
        
        result = []

        with open('./OutputService/Outputs/Output_Raw.csv', 'r') as file:
            for line in file.readlines():
                result.append(self.parseLine(line))

        r = "".join(map(str, result))        
                 
        with open('./OutputService/Outputs/Output_Clean.csv', 'w+') as file:
            file.write(r) 

        df = pd.read_csv("./OutputService/Outputs/Output_Clean.csv", sep=";", header=None)
        df.to_csv("./OutputService/Outputs/Output_Clean.csv", header=["Approach", "Subject", "Predicate", "Object", "Score"], index=False)
    

    def parseLine(self, line:str):
        line = line.replace('(', '')
        line = line.replace("'", '')
        line = line.replace(')', '')
        line = line.replace('<', '')    
        line = line.replace('>', '')
        line = line.replace(', ', ';')
        return(line) 
