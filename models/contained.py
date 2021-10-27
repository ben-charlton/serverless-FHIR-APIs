from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
import json
from models.base import BaseModel

class Contained(BaseModel, object):
    __tablename__ = "Contained"
    id = Column(Integer, primary_key=True)
    response_id = Column(String(100), ForeignKey('QuestionnaireResponse.uid' )) 
    response = relationship("QuestionnaireResponse", back_populates="contained", passive_deletes=True)
    string = Column(String)

    def __init__(self):
        self.response_id = None
        self.string = None
    
    def update(self, response_id, resource_dict):
        self.response_id = response_id
        self.string = json.dumps(resource_dict, indent=4)
        return

    def to_dict(self):
        return json.loads(self.string)

    def _save(self, session):
        session.add(self)
        return