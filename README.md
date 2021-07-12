# serverless-FHIR-APIs

A serverless solution for the management of questionnaire resources based on the FHIR specification.

The microservices are housed within Microsoft Azure, utilising Azure Functions to expose the API's
and using Azure SQL Database as the persistence provider.

## Capability Statement

Currently, there is support for the following API's under the FHIR specification;
- POST API : Support creation of Questionnaire Resource and store it internally for tracking administrations.

### Installing required modules
```bash
$ pip install -r requirements.txt
```
