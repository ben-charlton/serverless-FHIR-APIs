import logging
import json
import azure.functions as func

statement = {
  "resourceType": "CapabilityStatement",
  "version": "1.0.0",
  "name": "FHIR QAPI",
  "status": "active",
  "date": "02-11-2021",
  "publisher": "Ben Charlton",
  "contact": [
    {
      "name": "Ben Charlton"
    }
  ],
  "description": "This server implements the FHIR QAPI version 1.0.0",
  "kind": "capability",
  "software": {
    "name": "Azure Functions",
    "version": "4.0.0",
  },
  "fhirVersion": "4.0.1",
  "acceptUnknown": "both",
  "format": [
    "application/fhir+json"
  ],
  "profile": [
      { "reference": "https://www.hl7.org/fhir/questionnaire.html" },
      { "reference": "https://www.hl7.org/fhir/questionnaireresponse.html" }

  ],
  "rest": [
    {
      "mode": "server",
      "security": {
        "cors": "true"
      },
      "resource": [
        {
          "type": "Questionnaire",
          "interaction": [
            {
              "code": "create"
            },
            {
              "code": "read"
            },
            {
              "code": "search-type"
            },
            {
              "code": "delete"
            }
          ],
          "searchParam": [
            {
              "name": "uid",
              "type": "string",
              "documentation": "Questionnaire UID (i.e. https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire/123456789"
            },
            {
              "name": "id",
              "type": "string",
              "documentation": "Questionnaire ID (i.e. https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire?id=123456789"
            },
            {
              "name": "name",
              "type": "string",
              "documentation": "Questionnaire Name (i.e. https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire?name=quest1"
            },
            {
              "name": "url",
              "type": "string",
              "documentation": "Questionnaire URL (i.e. https://fhir-questionnaire-api.azurewebsites.net/api/questionnaire?url=123456789"
            },
          ]
        },
        {
          "type": "QuestionnaireResponse",
          "interaction": [
            {
              "code": "create"
            },
            {
              "code": "read"
            },
            {
              "code": "search-type"
            },
            {
              "code": "delete"
            }
          ],
          "searchParam": [
            {
              "name": "uid",
              "type": "string",
              "documentation": "Questionnaire UID (i.e. https://fhir-questionnaire-api.azurewebsites.net/api/questionnaireResponse/123456789"
            }
          ]
        }
      ]
    }
  ]
}

def main(req: func.HttpRequest) -> func.HttpResponse:

    if statement:
        return func.HttpResponse(body=json.dumps(statement, indent=4), status_code=200)
    else:
        return func.HttpResponse(status_code=500)

