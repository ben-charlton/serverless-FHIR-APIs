from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict
from questionnaire import BaseModel

### CODING CLASS DEFINITION
### This is the ORM mapped class that is used to create
### coding objects that compose some Questionnaire elements
class Coding(BaseModel, object):
    
    __tablename__ = "Coding"
    id = Column(Integer, primary_key=True)
    questionnaireId = Column(String(450), ForeignKey('Questionnaire.id'))
    itemId = Column(Integer, ForeignKey('QuestionnaireItem.id'))
    system = Column(String)
    version = Column(String)
    code = Column(String)
    display = Column(String)
    userSelected = Column(Boolean)
    
    def __init__(self):
        
        self.system = None
        self.version = None
        self.code = None
        self.display = None
        self.userSelected = None

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "id" or key == "questionnaireId" or key == "itemId":
                pass
            else:
                if getattr(self, key) is not None:
                    result[key] = getattr(self, key)
        return result

    def update_with_dict(self, json_dict):
        for key in json_dict:
            setattr(self, key, json_dict[key])
        return

    def _save(self, session):
        session.add(self)
        return
        
