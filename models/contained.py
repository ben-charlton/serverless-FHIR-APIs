from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
import json


class Contained(BaseModel, object):
    __tablename__ = "Contained"
    id = Column(Integer, primary_key=True)
    response_id = (String(450), ForeignKey("QuestionnaireResponse.id")) 
    string = Column(String)

    def __init__(self, response_id, resource_dict):
        self.response_id = response_id
        self.string = json.dumps(resource_dict)

    def to_dict(self):
        return json.loads(self.string, indent=4)

    def _save(self, session):
        session.add(self)
        return