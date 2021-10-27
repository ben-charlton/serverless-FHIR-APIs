from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict
from models.base import BaseModel



### CODING CLASS DEFINITION
### This is the ORM mapped class that is used to create
### coding objects that compose some Questionnaire elements
class Coding(BaseModel, object):
    
    __tablename__ = "Coding"
    id = Column(Integer, primary_key=True)
    quid = Column(String(100), ForeignKey('Questionnaire.uid', ondelete="cascade"))
    iid = Column(Integer, ForeignKey('QuestionnaireItem.id', ondelete="cascade"))
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
            if key == "id" or key == "quid" or key == "iid":
                pass
            else:
                if getattr(self, key) is not None:
                    result[key] = getattr(self, key)
        return result

    def update_with_dict(self, json_dict):
        VALID_ELEMENTS = ["system", "version", "code", "display", "userSelected"]
        for key in json_dict:
            if key in VALID_ELEMENTS:
                setattr(self, key, json_dict[key])
            else:
                raise Exception("JSON object must be a Questionnaire resource")
        return

    def _save(self, session):
        session.add(self)
        return
        
