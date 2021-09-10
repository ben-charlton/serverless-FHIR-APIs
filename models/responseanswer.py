from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict

class QuestionnaireResponseItemAnswer(BaseModel, object):
    __tablename__ = "ResponseItemAnswer"
    id = Column(Integer, primary_key=True)
    valueBoolean = Column(Boolean)
    valueDecimal = Column(Float)
    valueInteger = Column(Integer)
    valueDate = Column(Date)
    valueDateTime = Column(DateTime)
    valueTime = Column(DateTime)
    valueString = Column(String)
    valueUri = Column(String)
    valueAttachment = Column(String)
    valueCoding = Column(String)
    valueQuantity = Column(String)
    valueReference = Column(String)
    item = relationship('QuestionnaireResponseItem', back_populates="questionnaireResponse", lazy = True)

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
        self.item = []

    def update_with_dict(self, item_dict):
        for key in item_dict:
            if key == "item":
                items_list = item_dict[key]
                for single_item_dict in items_list:
                    new_item = QuestionnaireResponseItem()
                    new_item.update_with_dict(single_item_dict, response_id, item_dict['linkId'])
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