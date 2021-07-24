
from stringtest import Questionnaire
import json
import pickle
from collections import OrderedDict
from sqlalchemy import inspect

json_dict = { "id": "16",
  "name": "questionnaire with item recursive",
  "url": "www.testurl.com",
  "title": "checking two element item list",
  "item": [
        {
          "linkId": "linkid1",
          "text": "outer item 1",
          "item": [
                {
                  "linkId": "linkid11",
                  "text": "innner item 1",
                },
                {
                  "linkId": "linkid12",
                  "text": "innner item 2",
                },
                {
                  "linkId": "linkid13",
                  "text": "innner item 3",
                  "item": [{
                          "linkId": "linkid131",
                          "text": "innner item 3.1",
                          }]
                }]
        },
        {
          "linkId": "linkid2",
          "text": "outer item 2",
          "item": [
                {
                  "linkId": "linkid2.1",
                  "text": "inner item 2",
                  "item": [{
                          "linkId": "linkid2.1.1",
                          "text": "innner item 1",
                  }]
                }]
        }
        ]  
}

test_questionnaire = Questionnaire()
#test_questionnaire.update_with_json(json_dict)
val = test_questionnaire.load("id", 16)
#val = test_questionnaire.save()
print(val)




# def _to_dict(obj):
#   result = OrderedDict()
#   for key in obj.__mapper__.c.keys():
#     if key == "item":
#       result["item"] = key._to_dict()
#     else:
#       result[key] = getattr(obj, key)
#   return result

# with open('obj.dictionary', 'rb') as config_dictionary_file:
#   quest = pickle.load(config_dictionary_file)
 
#   mapper = inspect(quest)
#   for key in mapper.attrs:
#         print(key.value)
