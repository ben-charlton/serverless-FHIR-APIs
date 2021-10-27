from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict
from models.base import BaseModel
import json
from models.responseitem import QuestionnaireResponseItem
class QuestionnaireResponseItemAnswer(BaseModel, object):
    __tablename__ = "QuestionnaireResponseItemAnswer"
    id = Column(Integer, primary_key=True)
    item_FK = Column(Integer, ForeignKey('QuestionnaireResponseItem.id', ondelete="cascade"))
    item_id = Column(String)
    answer_counter = Column(Integer)
    valueBoolean = Column(Boolean)
    valueDecimal = Column(Float)
    valueInteger = Column(Integer)
    valueDate = Column(String)
    valueDateTime = Column(String)
    valueTime = Column(String)
    valueString = Column(String)
    valueUri = Column(String)
    valueAttachment = Column(String)
    valueCoding = Column(String)
    valueQuantity = Column(String)
    valueReference = Column(String)
    
    def __init__(self):
        
        self.valueBoolean = None
        self.valueDecimal = None
        self.valueInteger = None
        self.valueDate = None
        self.valueDateTime = None
        self.valueTime = None
        self.valueString = None
        self.valueUri = None
        self.valueAttachment = None
        self.valueCoding = None
        self.valueQuantity = None
        self.valueReference = None
        self.item_id = None
        self.answer_counter = None
        self.item = []

    def update_with_dict(self, json_dict, response_id, item_id, answer_counter=None):
        VALID_ELEMENTS = ["valueBoolean", "valueDecimal", "valueInteger", "valueDate", "valueDateTime", "valueTime", "valueString", "valueUri"]
        self.item_id = item_id
        self.answer_counter = answer_counter
        for key in json_dict:
            if key == "valueAttachment" or key == "valueCoding" or key == "valueQuantity" or key == "valueReference":
                setattr(self, key, json.dumps(json_dict[key], indent=4))
            elif key == "item":
                items_list = json_dict[key]
                for single_item_dict in items_list:
                    new_item = QuestionnaireResponseItem()
                    new_item.update_with_dict(single_item_dict, response_id, item_id, answer_counter)
                    self.item.append(new_item)  
            else:
                if key in VALID_ELEMENTS:
                    setattr(self, key, json_dict[key])
                else:
                    raise Exception("JSON object must be a QuestionnaireResponse resource")
        return

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if attribute.value == None:
                continue
            if key == "item_FK" or key == "id":
                pass
            elif key == "valueAttachment" or key == "valueCoding" or key == "valueQuantity" or key == "valueReference":
                result[key] = json.loads(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

    def _save(self, session):
        session.add(self)
        for item in self.item:
            item._save(session)
        return