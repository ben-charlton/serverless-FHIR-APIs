# import json
# from questionnaire import Questionnaire

# class QuestionnaireEncoder(JSONEncoder):
#     def encode(self, o):
#         if isinstance(o, Questionnaire):
#             return o.__dict__
#         else:
#             # call base class implementation which takes care of
#             # raising exceptions for unsupported types
#             return json.JSONEncoder.default(self, object)

