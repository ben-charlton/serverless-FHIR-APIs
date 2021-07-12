import logging
import json
import azure.functions as func
import os
import pyodbc
from models.questionnaire import Questionnaire


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    retrieved_questionnaire_json = None
    search_parameter = req.params.get('paramter')
    search_value = req.params.get('value')
    retrieved_questionnaire = Questionnaire()
    retrieved_questionnaire_json = retrieved_questionnaire.load(search_parameter, search_value)

    if retrieved_questionnaire_json is not None: 
        return func.HttpResponse(json.dumps(retrieved_questionnaire_json), headers={"content-type": "application/json"}, status_code=200)
    else:
        return func.HttpResponse(body="get request failed", status_code=500)
