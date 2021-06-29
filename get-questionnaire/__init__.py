import logging
import json
import azure.functions as func
import os
import pyodbc


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    sqlConnectionString = os.environ["serverlessdb"]

    try:
        questionnaireToRetrieve = req.params.get('id')
        logging.info(questionnaireToRetrieve)
    except:
        return generateHttpResponse(ingredients, messages, 400)

    sqlConnection = getSqlConnection(sqlConnectionString)
    questionnaire = getQuestionnaire(sqlConnection, searchTerm)

    return generateHttpResponse(ingredients, messages, statusCode)

def generateHttpResponse(ingredients, messages, statusCode):
    return func.HttpResponse(
        json.dumps({"Messages": messages, "Questionnaire": ingredients}, sort_keys=True, indent=4),
        status_code=statusCode
    )

def getSqlConnection(sqlConnectionString):
    i = 0
    while i < 6:
        logging.info('contacting DB')
        try:
            sqlConnection = pyodbc.connect(sqlConnectionString)
        except:
            time.sleep(10) # wait 10s before retry
            i+=1
        else:
            return sqlConnection

def getQuestionnaire(sqlConnection, searchTerm):
    logging.info('getting questionnaire')
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute('search for ')
    questionnaire = json.loads(sqlCursor.fetchone()[0])
    sqlCursor.commit()
    sqlCursor.close()
    return questionnaire