from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.orm import relationship, Session
import urllib
import pyodbc
import json
from collections import OrderedDict
from functools import cmp_to_key
import uuid
import time
import os
import logging
from models.user import User
from models.answeroption import QuestionnaireItemAnswerOption
from models.coding import Coding
from models.enablewhen import QuestionnaireItemEnableWhen
from models.initial import QuestionnaireItemInitial
from models.questionnaireitem import QuestionnaireItem
from models.base import BaseModel



### QUESTIONNAIRE CLASS DEFINITION
### This is the ORM mapped class that is used to create
### questionnaire objects from a given JSON body (POST),
### and stored in the SQL database to be retrieved (GET)
class Questionnaire(BaseModel, object):
    
    ### The ORM mapping for the object 
    ### This creates the table in the database (once only)
    ### and sets up the mapping from object->database
    __tablename__ = "Questionnaire"
    resourceType = Column(String)
    uid = Column(String(100), primary_key=True)
    id = Column(String) 
    user_id = Column(String)
    text = Column(String)
    contained = Column(String)
    meta = Column(String)
    Identifier = Column(String)
    url = Column(String)
    extension = Column(String)
    version = Column(String)
    effectivePeriod = Column(String)
    derivedFrom = Column(String)
    useContext = Column(String)
    name = Column(String)
    title = Column(String)
    subjectType = Column(String)
    status = Column(String)
    date = Column(String)
    publisher = Column(String)
    description = Column(String)
    purpose = Column(String)
    copyright = Column(String)
    code = relationship("Coding", lazy=True, cascade="all, delete", passive_deletes=True)
    item = relationship('QuestionnaireItem', back_populates="questionnaire", lazy = True)

    def __init__(self):
        self.resourceType = "Questionnaire"
        self.uid = uuid.uuid4().hex
        self.id = None
        self.user_id = None
        self.text = None
        self.contained = None
        self.meta = None
        self.effectivePeriod = None
        self.derivedFrom = None
        self.useContext = None
        self.version = None
        self.Identifier = None
        self.extension = None
        self.subjectType = None
        self.url = None
        self.name = None 
        self.title = None
        self.status = None # draft | active | retired | unknown
        self.date = None
        self.publisher = None
        self.purpose = None
        self.copyright = None
        self.code = []
        self.item = [] 


    ### This function takes in the posted JSON from the request
    ### and fills the newly created object with the data,
    ### setting each attribute to the respective field in the JSON
    def update_with_json(self, json_dict, user_id):
        VALID_ELEMENTS = ["id", "url", "name", "status", "date", "publisher", "description", "purpose", "copyright", "resourceType", "title", "version", "effectivePeriod"]
        self.user_id = user_id
        for key in json_dict:
            if key == "code":
                code_list = json_dict[key]
                for code_dict in code_list:
                    new_item = Coding()
                    new_item.update_with_dict(code_dict)
                    self.code.append(new_item)
            elif key == "text" or key == "subjectType" or key == "identifier" or key == "meta" or key == "contained" or key == "extension" or key == "derivedFrom" or key == "useContext":
                setattr(self, key, json.dumps(json_dict[key], indent=4))
            elif key == "item":
                items_list = json_dict[key]
                for item_dict in items_list:
                    new_item = QuestionnaireItem()
                    new_item.update_with_dict(item_dict, self.uid, None)
                    self.item.append(new_item)
            else:
                if key in VALID_ELEMENTS:
                    setattr(self, key, json_dict[key])
                else:
                    raise Exception("JSON object must be a Questionnaire resource")
        return

    ### Connects to the database given the authorised connection string
    ### and creates the tables if they are not already created, 
    ### before saving off the Questionnaire, and all attached child objects 
    def save(self):
        connect_str = self._get_conn_string()
        try: 
            return_uid = self.uid
            engine = create_engine(connect_str)
            BaseModel.metadata.create_all(engine)
            session = Session(engine)
            session.begin()
            user = session.query(User).filter_by(user_id=self.user_id).first()
            if (user is None):
                raise Exception("User not found")
            session.add(self)
            self._save_child_elements(session)
            session.commit()
            session.close()
            return return_uid
        except Exception as e:
            raise Exception(str(e))
            
            


    ### Takes in the query parameters from the GET request
    ### and returns the JSON form of the questionnaire requested 
    def load(self, query, user_id):
        connect_str = self._get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            user = session.query(User).filter_by(user_id=user_id).first()
            if (user is None):
                raise Exception("User not found")
            #kwargs = {param : value}
            if 'uid' in query.keys():
                retrieved_questionnaire = session.query(Questionnaire).filter_by(**query, user_id=user_id).one()
                retrieved_json = retrieved_questionnaire._to_json()
            else:
                retrieved_questionnaires = session.query(Questionnaire).filter_by(**query, user_id=user_id).all()
                retrieved_json = []
                for ques in retrieved_questionnaires:
                    json_dict = ques._to_dict()
                    retrieved_json.append(json_dict)
                retrieved_json = json.dumps(retrieved_json, indent=4)
            session.close()
            return retrieved_json
        except Exception as e:
            raise Exception(str(e))

    def delete(self, uid, user_id):
        connect_str = self._get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            user = session.query(User).filter_by(user_id=user_id).first()
            if (user is None):
                raise Exception("User not found")
            z = session.query(QuestionnaireItem).filter(QuestionnaireItem.quid==uid).delete()
            r = session.query(Questionnaire).filter(Questionnaire.uid==uid).delete()
            if (r == 0):
                raise Exception("No resource with matching uid found")
            session.commit()
            session.close()
            return True
        except Exception as e:
            raise Exception(str(e))


    ### Saves all child elements associated with the Questionnaire
    ### by recursively adding all items and codes.
    def _save_child_elements(self, session):
        for item in self.item:
            item._save(session)
        for code in self.code:
            code._save(session)
        return

    ### converts the Questionnaire object into a dictionary 
    ### that can then be JSONified and returned through a (GET)
    def _to_dict(self):
        try:
            result = OrderedDict() 
            mapper = inspect(self)
            for attribute in mapper.attrs:   
                key = attribute.key
                if attribute.value == None or key == "uid" or key == "user_id":
                    continue
                if key == "item":
                    result[key] = self._build_item_list(attribute.value)
                elif key == "text" or key == "subjectType" or key == "identifier" or key == "meta" or key == "contained" or key == "extension" or key == "derivedFrom" or key == "useContext":
                    result[key] = json.loads(getattr(self, key))
                elif key == "code":
                    code_list = []
                    for entry in attribute.value:
                        code_list.append(entry.to_dict())
                    if len(code_list) > 0:
                        result[key] = code_list
                else:
                    result[key] = getattr(self, key)
        except Exception as e:
            raise Exception(str(e))

        return result
   
   
   ### return the Questionnaire in a JSON format
    def _to_json(self):
        return json.dumps(self._to_dict(), indent=4)

    
    ### Return the list of questionnaire items 
    ### in json format of nested dicts
    ### to be returned 
    def _build_item_list(self, list_of_items):

        list_of_dicts = self._item_to_dict(list_of_items)
        parent_list = []
        nesting_check = 0
        
        try:
            for entry in list_of_dicts:
                if entry["parent_id"] != None:
                    nesting_check = 1
                else:
                    parent_list.append(entry)
                entry["item"] = []
            while (nesting_check == 1):
                nesting_check = 0
                for item1 in list_of_dicts:
                    for item2 in list_of_dicts:
                        if  item1["parent_id"] is not None and item1["parent_id"] == item2["linkId"]:
                            item1["parent_id"] = None
                            item2["item"].append(item1)
                            nesting_check = 1

            for entry in list_of_dicts:
                del entry["parent_id"]
                if len(entry["item"]) == 0:
                    del entry["item"]
        except Exception as e:
            raise Exception(str(e) + "here")

        return parent_list

    ### create the connection string for the database
    ### which will eventually take in an authorised token
    def _get_conn_string(self):
        odbc_str = os.environ["SQL_CONNECTION_STRING"] 
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        return connect_str


    ### helper function to create the list of item dicts
    ### that gets processed to produce the final list
    @staticmethod
    def _item_to_dict(item_list):
        dict_list = []
        for item in item_list:
            dict_to_add = item.to_dict()
            dict_list.append(dict_to_add)
        return dict_list
