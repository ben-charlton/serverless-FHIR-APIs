from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict

class QuestionnaireItemEnableWhen(BaseModel):
    __tablename__ = "QuestionnaireItemEnableWhen"
    id = Column(Integer, primary_key=True)
    item = relationship("QuestionnaireItem", back_populates="enableWhen")
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
    
    def save(self, session):
        session.add(self)
        return

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "item" or key == "id":
                pass
            else:
                if getattr(self, key) is not None:
                    result[key] =  getattr(self, key)
        return result