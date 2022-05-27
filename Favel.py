import configparser, logging, argparse

from FactValidationService.Validator import Validator
from InputService.Input import Input

def main():
    # Parse arguments
    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("-d", "--data", required=True, help="Path to input data")
    args = argumentParser.parse_args()
    
    # Read config
    configParser = configparser.ConfigParser()
    configParser.read("favel.conf")

    # Configure logging
    loggingOptions = dict()
    loggingOptions['debug'] = logging.DEBUG
    loggingOptions['info'] = logging.INFO
    loggingOptions['error'] = logging.ERROR
    loggingOptions['critical'] = logging.CRITICAL
    
    logging.basicConfig(level=loggingOptions[configParser['General']['logging']])
    
    
    # Example assertion
    assertions = [
        ("<http://dbpedia.org/resource/Al_Attles>", "<http://dbpedia.org/ontology/team>", "<http://dbpedia.org/resource/Golden_State_Warriors>")
        ]
    
    # Read input
    input = Input()
    assertions = input.getInput(args.data)

    # Validate assertions
    logging.info("Validating assertions")
    validator = Validator(dict(configParser['Approaches']))
    result = validator.validate(assertions)
    
    # Print results
    print(result)
    

if __name__ == '__main__':
    main()