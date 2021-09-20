<img src="https://miro.medium.com/max/1400/1*GfBkvGMAIH9ptyEB6rM5Tw.png" width="300" height="150">

# serverless-FHIR-APIs

A serverless solution for the management of questionnaire resources based on the [FHIR specification](https://www.hl7.org/fhir/).

The microservices are housed within Microsoft Azure, utilising Azure Functions to expose the API's
and using Azure SQL Database as the persistence provider.

## Capability Statement

Currently, there is support for the following API's under the FHIR specification;

1. [POST] https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire
  > Sends the Questionnaire resource specified in JSON format to the Azure SQL Database 
  > and returns the generated uid where it is stored. 
2. [GET] https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/{uid}
 > Returns the Questionnaire resource in JSON format specified by the uid.
3. [GET] https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire?name=&id=&title=
 > Returns the list of Questionnaire resources matching the query in JSON format.
4. [DELETE] https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/{uid}
  > Deletes the specified Questionnaire resource from the database.
5. [POST] https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse
  > Sends the QuestionnaireResponse resource specified in JSON format to the Azure SQL Database 
  > and returns the generated uid where it is stored. 
6. [GET] https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/{uid}
 > Returns the QuestionnaireResponse resource in JSON format specified by the uid.
7. [GET] https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse?name=&id=&title=
 > Returns the list of QuestionnaireResponse resources matching the query in JSON format.
8. [DELETE] https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/{uid}
  > Deletes the specified QuestionnaireResponse resource from the database.


### Installing required modules to work with the 
```bash
$ pip install -r requirements.txt
```

