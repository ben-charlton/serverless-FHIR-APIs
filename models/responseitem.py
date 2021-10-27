from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict
import json
from models.base import BaseModel
from models.responseanswer import QuestionnaireResponseItemAnswer

class QuestionnaireResponseItem(BaseModel, object):
    __tablename__ = "QuestionnaireResponseItem"
    id = Column(Integer, primary_key=True)
    response_id = Column(String(100), ForeignKey('QuestionnaireResponse.uid', ondelete="cascade"))
    questionnaireResponse = relationship("QuestionnaireResponse", cascade='delete', back_populates="item", foreign_keys=[response_id], passive_deletes=True)
    parent_id = Column(String)
    linkId = Column(String)
    definition = Column(String)
    text = Column(String)
    answer_id = Column(Integer)
    answer = relationship("QuestionnaireResponseItemAnswer", cascade='delete', passive_deletes=True)


    def __init__(self):
       
        self.linkId = None
        self.definition = None
        self.text = None
        self.answer = []
        self.item = []
        self.response_id = None
        self.parent_id = None
        self.answer_id = None

    def update_with_dict(self, item_dict, response_id, parent_id=None, answer_id=None):
        VALID_ELEMENTS = ["linkId", "definition", "text"]
        self.response_id = response_id
        self.parent_id = parent_id
        self.answer_id = answer_id
        for key in item_dict:
            if key == "answer":
                answer_list = item_dict[key]
                answer_counter = 1
                for entry in answer_list:
                    answer = QuestionnaireResponseItemAnswer()
                    answer.update_with_dict(entry, response_id, item_dict["linkId"], answer_counter)
                    self.answer.append(answer)
                    answer_counter = answer_counter + 1
            elif key == "item":
                items_list = item_dict[key]
                for single_item_dict in items_list:
                    new_item = QuestionnaireResponseItem()
                    new_item.update_with_dict(single_item_dict, response_id, item_dict["linkId"])
                    self.item.append(new_item)  
            else:
                if key in VALID_ELEMENTS:
                    setattr(self, key, item_dict[key])
                else:
                    raise Exception("JSON object must be a QuestionnaireResponse resource")
        return

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "questionnaireResponse" or key == "id" or key == "answer" or key == "response_id":
                continue
            if (key == "definition" or key == "text") and attribute.value == None:
                continue
            else:
                result[key] = getattr(self, key)
        return result

    def _save(self, session):
        session.add(self)
        for item in self.item:
            item._save(session)
        for answer in self.answer:
            answer._save(session)
        return