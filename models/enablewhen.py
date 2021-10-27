from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict
import json
from models.base import BaseModel

class QuestionnaireItemEnableWhen(BaseModel,object):
    __tablename__ = "QuestionnaireItemEnableWhen"
    id = Column(Integer, primary_key=True)
    iid = Column(Integer, ForeignKey('QuestionnaireItem.id', ondelete="cascade"))
    question = Column(String)
    operator = Column(String)
    answerBoolean = Column(Boolean)
    answerDecimal = Column(Float)
    answerInteger = Column(Integer)
    answerDate = Column(Date)
    answerDateTime = Column(DateTime)
    answerString = Column(String)
    answerCoding = Column(String)

    def __init__(self):
        self.question = None
        self.operator = None
        self.answerBoolean = None
        self.answerDecimal = None
        self.answerInteger = None
        self.answerDate = None
        self.answerDateTime = None
        self.answerString = None
        self.answerCoding = None

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "iid" or key == "id":
                pass
            else:
                if getattr(self, key) is not None:
                    if key == "answerCoding":
                        result[key] = json.loads(attribute.value)
                    else:
                        result[key] =  getattr(self, key)
        return result

    def update_with_dict(self, json_dict):
        VALID_ELEMENTS = ["question", "operator", "answerBoolean", "answerInteger", "answerDate", "answerDateTime", "answerString", "answerCoding"]
        for key in json_dict:
            if key == "answerCoding":
                self.answerCoding = json.dumps(json_dict[key])
            else:
                if key in VALID_ELEMENTS:
                    setattr(self, key, json_dict[key])      
                else:
                    raise Exception("JSON object must be a Questionnaire resource")
        return
    
    def _save(self, session):
        session.add(self)
        return