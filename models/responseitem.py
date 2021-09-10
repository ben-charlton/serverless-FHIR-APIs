from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict

class QuestionnaireResponseItem(BaseModel, object):
    __tablename__ = "ResponseItem"
    id = Column(Integer, primary_key=True)
    QuestionnaireResponse = relationship("QuestionnaireResponse", back_populates="item")
    response_id = Column(String(450), ForeignKey('QuestionnaireResponse.id'))
    parent_id = Column(String, ForeignKey('QuestionnaireResponseItem.linkId'))
    answer_id = Column(Integer, ForeignKey('ResponseItemAnswer.id'))
    linkId = Column(String)
    definition = Column(String)
    text = Column(String)
    answer = relationship("ResponseItemAnswer")

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
        self.response_id = response_id
        if parent_id is not None:
            self.parent_id = parent_id
        if answer_id is not None:
            self.answer_id = answer_id
        for key in item_dict:
            if key == "answer":
                answer_list = item_dict[key]
                for entry in answer_list:
                    answer = QuestionnaireResponseItemAnswer()
                    answer.update_with_dict(entry)
                    self.answer.append(answer)
            elif key == "item":
                items_list = item_dict[key]
                for single_item_dict in items_list:
                    new_item = QuestionnaireResponseItem()
                    new_item.update_with_dict(single_item_dict, response_id, parent_id, answer_id)
                    self.item.append(new_item)  
            else:
                setattr(self, key, item_dict[key])
        return

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "questionnaire" or key == "questionnaire_id" or key == "dummyCol":
                pass
            else:
                result[key] = getattr(self, key)
                # will need to see if this works for all of the lists?
        return result

    def _save(self, session):
        session.add(self)
        for item in self.item:
            item._save(session)
        for answer in self.answer:
            answer._save(session)
        return