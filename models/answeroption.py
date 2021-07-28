from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict
from questionnaire import BaseModel
class QuestionnaireItemAnswerOption(BaseModel, object):
    __tablename__ = "QuestionnaireItemAnswerOption"
    id = Column(Integer, primary_key=True)
    itemId = Column(Integer, ForeignKey('QuestionnaireItem.id'))
    valueInteger = Column(Integer)
    valueDate = Column(Date)
    valueTime = Column(DateTime)
    valueString = Column(String)
    valueCoding = Column(String)
    initialSelected = Column(Boolean)

    def __init__(self):
        self.id = None
        self.valueInteger = None
        self.valueDate = None
        self.valueDateTime = None
        self.valueString = None
        self.valueCoding = None
        self.initialSelected = None

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "itemId" or key == "id":
                pass
            else:
                if getattr(self, key) is not None:
                    if key == "valueCoding":
                        result[key] = json.loads(getattr(self, key))
                    else:
                        result[key] =  getattr(self, key)
        return result

    def update_with_dict(self, json_dict):
        for key in json_dict:
            if key == "valueCoding":
                setattr(self, key, json.dumps(json_dict[key]))      
            else:
                setattr(self, key, json_dict[key])       
        return

    def _save(self, session):
        session.add(self)
        return
    