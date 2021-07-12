import json

class QuestionnaireEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__