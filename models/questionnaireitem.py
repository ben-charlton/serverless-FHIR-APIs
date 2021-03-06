from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict
from .enablewhen import QuestionnaireItemEnableWhen
from .initial import QuestionnaireItemInitial
from .answeroption import QuestionnaireItemAnswerOption
from .coding import Coding
import json
from models.base import BaseModel

class QuestionnaireItem(BaseModel, object):
    __tablename__ = "QuestionnaireItem"
    id = Column(Integer, primary_key=True)
    questionnaire = relationship("Questionnaire", back_populates="item")
    quid = Column(String(100), ForeignKey('Questionnaire.uid'))
    parent_id = Column(String)
    linkId = Column(String)
    definition = Column(String)
    code = relationship("Coding", cascade="all, delete", passive_deletes=True)
    prefix = Column(String)
    text = Column(String)
    extension = Column(String)
    type = Column(String)
    enableWhen = relationship("QuestionnaireItemEnableWhen", cascade="all, delete", passive_deletes=True)
    enableBehavior = Column(String)
    required = Column(Boolean)
    repeats = Column(Boolean)
    readOnly = Column(Boolean)
    maxLength = Column(Integer)
    answerValueSet = Column(String)
    answerOption = relationship("QuestionnaireItemAnswerOption", cascade="all, delete", passive_deletes=True)
    initial = relationship("QuestionnaireItemInitial", cascade="all, delete", passive_deletes=True)


    def __init__(self):
        self.quid = None
        self.linkId = None
        self.definition = None
        self.code = []
        self.prefix = None
        self.text = None
        self.extension = None
        self.type = None
        self.enableWhen = []
        self.enableBehavior = None
        self.required = None
        self.repeats = None
        self.readOnly = None
        self.maxLength = None
        self.answerValueSet = None
        self.answerOption = []
        self.initial = []
        self.item = []

    def update_with_dict(self, item_dict, quid, parent_id=None):
        self.quid = quid
        self.parent_id = parent_id
        VALID_ELEMENTS = ["linkId", "definition", "prefix", "text", "type", "enableBehavior", "required", "repeats", "readOnly", "maxLength", "answerValueSet"]
        for key in item_dict:
            if key == "enableWhen":
                enable_list = item_dict[key]
                for entry in enable_list:
                    enable = QuestionnaireItemEnableWhen()
                    enable.update_with_dict(entry)
                    self.enableWhen.append(enable)
            elif key == "answerOption":
                answer_list = item_dict[key]
                for entry in answer_list:
                    answer = QuestionnaireItemAnswerOption()
                    answer.update_with_dict(entry)
                    self.answerOption.append(answer)
            elif key == "initial":
                initial_list = item_dict[key]
                for entry in initial_list:
                    initial = QuestionnaireItemInitial()
                    initial.update_with_dict(entry)
                    self.initial.append(initial)
            elif key == "item":
                items_list = item_dict[key]
                for single_item_dict in items_list:
                    new_item = QuestionnaireItem()
                    new_item.update_with_dict(single_item_dict, quid, item_dict['linkId'])
                    self.item.append(new_item)  
            elif key == "code":
                code_list = item_dict[key]
                for entry in code_list:
                    code = Coding()
                    code.update_with_dict(entry)
                    self.code.append(code)
            elif key == "extension":
                setattr(self, key, json.dumps(item_dict[key], indent=4))
            else:
                if key in VALID_ELEMENTS:
                    setattr(self, key, item_dict[key])
                else:
                    raise Exception("JSON object must be a Questionnaire resource")

        if self.linkId == None:
            raise Exception("Questionnaire Items must contain a linkId")

        return

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "questionnaire" or key == "quid" or key == "id":
                pass
            elif key == "parent_id":
                result[key] = getattr(self, key)
            else:
                if getattr(self, key) is not None:
                    if key == "extension":
                        result[key] = json.loads(getattr(self, key))    
                    elif isinstance(getattr(self, key), list):
                        if len(getattr(self, key)) > 0:
                            result_list = []
                            for entry in getattr(self, key):
                                result_list.append(entry.to_dict())
                            result[key] = result_list
                            
                    else:
                        result[key] = getattr(self, key)
    
        return result

    def _save(self, session):
        session.add(self)
        for item in self.item:
            item._save(session)
        for enable in self.enableWhen:
            enable._save(session)
        for code in self.code:
            code._save(session)
        for initial in self.initial:
            initial._save(session)
        for answer in self.answerOption:
            answer._save(session)
        return