# serverless-FHIR-APIs

A serverless solution for the management of questionnaire resources based on the FHIR specification.

## Capability Statement

Currently, there is support for the following API's under the FHIR specification;
•	POST API : Support creation of Questionnaire Resource and store it internally for tracking administrations.
    POST [BaseURL]/Questionnaire/ - Submit payload (body) of Questionnaire in JSON format.
•	GET API : Will be used to download a specific Questionnaire by authorized systems and personnel.
    GET [BaseURL]/Questionnaire/1234 - Receive a payload (body) of Questionnaire in JSON format.
    GET [BaseURL]/Questionnaire/?_summary=true - Receive all Questionnaires present in the system in summary format.
•	POST API : Support collection of PRO Responses using QuestionnaireResponse Resource and store it internally for tracking administrations.
    POST [BaseURL]/QuestionnaireResponse/ - Submit payload (body) of QuestionnaireResponse in JSON format.
•	GET API : Will be used to download a specific QuestionnaireResponse (PRO Responses) by authorized systems and personnel.
    GET [BaseURL]/QuestionnaireResponse/1234 - Receive a payload (body) of QuestionnaireResponse in JSON format.
•	Search API - Find Specific QuestionnaireResponses.
    GET [BaseURL]/QuestionnaireResponse?patient=1234 - Receive all QuestionnaireResponses for a patient

### Installing required modules
```bash
$ pip install -r requirements.txt
```
