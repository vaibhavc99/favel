import logging

class Input:
    # TODO: this is just an example method
    
    def getInput(self, filePath:str):
        result = []
        with open(filePath, 'r') as file:
            for line in file.readlines():
                result.append(self.parseLine(line))
        logging.info("Read {} assertions".format(len(result)))
        return result 
                
    def parseLine(self, line:str):
        line = line.replace('\n', '')
        line = line.replace('"', '')
        elements = line.split(' ')
        return (elements[0], elements[1], elements[2][:-1])