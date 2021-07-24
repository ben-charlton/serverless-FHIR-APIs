from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict


BaseModel = declarative_base(name='BaseModel')

### CODING CLASS DEFINITION
### This is the ORM mapped class that is used to create
### coding objects that compose some Questionnaire elements
class Coding(BaseModel, object):
    
    __tablename__ = "Coding"
    id = Column(Integer, primary_key=True)
    questionnaire = relationship("Questionnaire", back_populates="code")
    item = relationship("QuestionnaireItem", back_populates="code")
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
            if key == "id" or key == "questionnaire" or key == "item":
                pass
            else:
                result[key] = getattr(self, key)
        return result

    def update_with_json(self, json_dict):
        for key in json_dict:
            setattr(self, key, json_dict[key])
        return

    def save(self, session):
        session.add(self)
        return
        
        