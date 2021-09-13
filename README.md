# serverless-FHIR-APIs

A serverless solution for the management of questionnaire resources based on the [FHIR specification](https://www.hl7.org/fhir/).

The microservices are housed within Microsoft Azure, utilising Azure Functions to expose the API's
and using Azure SQL Database as the persistence provider.

## Capability Statement

Currently, there is support for the following API's under the FHIR specification;

1. [GET] https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/{uid}
 > Returns the Questionnaire resource in JSON format specified by the uid
2. [POST] https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire


### Installing required modules
```bash
$ pip install -r requirements.txt
```

