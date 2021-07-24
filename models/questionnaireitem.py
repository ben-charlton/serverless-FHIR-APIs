from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
import urllib
import pyodbc
import json
from collections import OrderedDict
from functools import cmp_to_key
from coding import Coding
from enablewhen import QuestionnaireItemEnableWhen

class QuestionnaireItem(BaseModel):
    __tablename__ = "QuestionnaireItem"
    id = Column(Integer, primary_key=True)
    questionnaire = relationship("Questionnaire", back_populates="items")
    questionnaire_id = Column(String(450), ForeignKey('Questionnaire.id'))
    linkId = Column(String)
    definition = Column(String)
    enableWhen = relationship("QuestionnaireItemEnableWhen", back_populates="item", lazy = True)
    code = relationship("Coding", back_populates='item')
    text = Column(String)
    #prefix = Column(String)
    #enable_when = relationship("QuestionnaireItemEnableWhen", back_populates="item", uselist=False)

    def __init__(self):
        self.linkId = None
        self.questionnaire_id = None
        self.text = None
        self.items = []
        self.enable_when = [] # list represented in JSON as Dict
        self.prefix = None

    def update_with_dict(self, item_dict, questionnaire_id, parentId=None):
        self.questionnaire_id = questionnaire_id
        if parentId is not None:
            self.parentId = parentId
        for key in item_dict:
            if key == "enableWhen":
                enable_list = item_dict[key]
                for entry in enable_list:
                    enable_item = QuestionnaireItemEnableWhen()
                    enable_item.update_with_dict(entry)
                pass
            elif key == "answerOption":
                items_list = item_dict[key]
                for entry in enable_list:
                    enable_item = QuestionnaireItemEnableWhen()
                    enable_item.update_with_dict(entry)
                pass
            elif key == "initial":
                items_list = item_dict[key]
                for entry in enable_list:
                    enable_item = QuestionnaireItemEnableWhen()
                    enable_item.update_with_dict(entry)
                pass
            elif key == "item":
                items_list = item_dict[key]
                for single_item_dict in items_list:
                    new_item = QuestionnaireItem()
                    new_item.update_with_dict(single_item_dict, questionnaire_id, item_dict['linkId'])
                    self.items.append(new_item)  
            else:
                setattr(self, key, item_dict[key])
                
        return

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "questionnaire" or key == "questionnaire_id" or key == "dummyCol":
                # we do not want these values to be built in the dict
                # that represents the FHIR object
                # as they are not FHIR attributes
                pass
            else:
                result[key] = getattr(self, key)
        return result


    def build_enable_when_list(self):
        return

    def _save(self, session):
        session.add(self)
        for item in self.items:
            item._save(session)
        for enable in self.enableWhen:
            enable.save(session)
        for code in self.code:
            code.save(session)
        return