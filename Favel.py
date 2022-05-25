import configparser, logging

from FactValidationService.Validator import Validator

def main():
    # Read config
    configParser = configparser.ConfigParser()
    configParser.read("favel.conf")

    # Configure logging
    loggingOptions = dict()
    loggingOptions['debug'] = logging.DEBUG
    loggingOptions['info'] = logging.INFO
    loggingOptions['error'] = logging.ERROR
    loggingOptions['critical'] = logging.CRITICAL
    
    logging.basicConfig(level=loggingOptions[configParser['Logging']['level']])
    
    
    # Example assertion
    assertions = [
        ("<http://dbpedia.org/resource/Al_Attles>", "<http://dbpedia.org/ontology/team>", "<http://dbpedia.org/resource/Golden_State_Warriors>")
        ]

    # Validate assertions
    logging.info("Validating assertions")
    validator = Validator(dict(configParser['Approaches']))
    result = validator.validate(assertions)
    
    # Print results
    print(result)
    

if __name__ == '__main__':
    main()