# serverless-FHIR-APIs

A serverless solution for the management of questionnaire resources based on the FHIR specification.

The microservices are housed within Microsoft Azure, utilising Azure Functions to expose the API's
and using Azure SQL Database as the persistence provider.

## Capability Statement

Currently, there is support for the following API's under the FHIR specification;
- POST API : Support creation of Questionnaire Resource and store it internally for tracking administrations.
- GET API : Support creation of Questionnaire Resource and store it internally for tracking administrations.
- POST API : Support creation of QuestionnaireResponse Resource and store it internally for tracking administrations.
- Get API : Support creation of QuestionnaireResponse Resource and store it internally for tracking administrations.


### Installing required modules
```bash
$ pip install -r requirements.txt
```

### To do:
1. Fix questionnaire not saving 
2. Finalise questionnaireResponse save/load
3. Sort out endpoint configuration and with that, figure out authorisation
4. Update/Delete's 
