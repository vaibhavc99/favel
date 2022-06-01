import configparser, logging, argparse

from FactValidationService.Validator import Validator
from InputService.Input import Input

def main():
    # Parse arguments
    args = parseArguments()
    
    # Read config
    configParser = loadConfig()

    # Configure logging
    configureLoggin(configParser)
    
    # Read input
    input = Input()
    assertions = input.getInput(args.data)

    # Validate assertions
    logging.info("Validating assertions")
    validator = Validator(dict(configParser['Approaches']), configParser['General']['cachePath'], configParser['General']['useCache'])
    result = validator.validate(assertions)
    
    # Write results
    # TODO: write results to file
    
def parseArguments():
    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("-d", "--data", required=True, help="Path to input data")
    return argumentParser.parse_args()
    
def loadConfig():
    configParser = configparser.ConfigParser()
    configParser.read("favel.conf")
    return configParser

def configureLoggin(configParser:configparser.ConfigParser):
    loggingOptions = dict()
    loggingOptions['debug'] = logging.DEBUG
    loggingOptions['info'] = logging.INFO
    loggingOptions['warning'] = logging.WARNING
    loggingOptions['error'] = logging.ERROR
    loggingOptions['critical'] = logging.CRITICAL
    
    logging.basicConfig(level=loggingOptions[configParser['General']['logging']])
    

if __name__ == '__main__':
    main()