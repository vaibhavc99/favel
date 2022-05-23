import configparser, logging

from FactValidationService.Validator import Validator

def main():
    # Read config
    logging.info("Reading configuration file")
    configParser = configparser.ConfigParser()
    configParser.read("favel.conf")
    
    # Example assertion
    assertions = [
        ("<http://dbpedia.org/resource/Al_Attles>", "<http://dbpedia.org/ontology/team>", "<http://dbpedia.org/resource/Golden_State_Warriors>")
        ]

    # Validate assertions
    logging.info("Validation assertions")
    validator = Validator(dict(configParser['Approaches']))
    result = validator.validate(assertions)
    
    # Print results
    print(result)
    

if __name__ == '__main__':
    main()