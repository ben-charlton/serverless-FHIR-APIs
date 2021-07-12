
from questionnaire import Questionnaire
import json

json_dict = { "id": "12345",
  "name": "test questionnaire",
  "url": "www.testurl.com",
  "title": "first test"
   }

#json_dict = json.loads(json_string)
test_questionnaire = Questionnaire()
test_questionnaire.update_with_json(json_dict)
test_questionnaire.save()

