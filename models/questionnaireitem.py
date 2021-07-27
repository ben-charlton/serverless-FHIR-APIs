from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict
from .questionnaire import BaseModel
from .enablewhen import QuestionnaireItemEnableWhen
from .initial import QuestionnaireItemInitial
from .answeroption import QuestionnaireItemAnswerOption
from .coding import Coding

class QuestionnaireItem(BaseModel, object):
    __tablename__ = "QuestionnaireItem"
    id = Column(Integer, primary_key=True)
    questionnaire = relationship("Questionnaire", back_populates="item")
    questionnaire_id = Column(String(450), ForeignKey('Questionnaire.id'))
    linkId = Column(String)
    definition = Column(String)
    code = relationship("Coding")
    prefix = Column(String)
    text = Column(String)
    type = Column(String)
    enableWhen = relationship("QuestionnaireItemEnableWhen")
    enableBehavior = Column(String)
    required = Column(Boolean)
    repeats = Column(Boolean)
    readOnly = Column(Boolean)
    maxLength = Column(Integer)
    answerValueSet = Column(String)
    answerOption = relationship("QuestionnaireItemAnswerOption")
    initial = relationship("QuestionnaireItemInitial")


    def __init__(self):
        self.questionnaire_id = None
        self.linkId = None
        self.definition = None
        self.code = []
        self.prefix = None
        self.text = None
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

    def update_with_dict(self, item_dict, questionnaire_id, parentId=None):
        self.questionnaire_id = questionnaire_id
        if parentId is not None:
            self.parentId = parentId
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
                    new_item.update_with_dict(single_item_dict, questionnaire_id, item_dict['linkId'])
                    self.item.append(new_item)  
            elif key == "code":
                code_list = item_dict[key]
                for entry in code_list:
                    code = Coding()
                    code.update_with_dict(entry)
                    self.code.append(code)
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
        for enable in self.enableWhen:
            enable._save(session)
        for code in self.code:
            code._save(session)
        for initial in self.initial:
            initial._save(session)
        for answer in self.answerOption:
            answer._save(session)
        return