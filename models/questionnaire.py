from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
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

BaseModel = declarative_base(name='BaseModel')

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
    text = Column(String)
    url = Column(String)
    name = Column(String)
    title = Column(String)
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
        self.text = None
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
    def update_with_json(self, json_dict):
        for key in json_dict:
            if key == "code":
                code_list = json_dict[key]
                for code_dict in code_list:
                    new_item = Coding()
                    new_item.update_with_dict(code_dict)
                    self.code.append(new_item)
            elif key == "text":
                setattr(self, key, json.dumps(json_dict[key], indent=4))
            elif key == "item":
                items_list = json_dict[key]
                for item_dict in items_list:
                    new_item = QuestionnaireItem()
                    new_item.update_with_dict(item_dict, self.uid, None)
                    self.item.append(new_item)
            else:
                setattr(self, key, json_dict[key])
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
            session.add(self)
            self._save_child_elements(session)
            session.commit()
            session.close()
            return return_uid
        except Exception as e:
            print(e)
            return False


    ### Takes in the query parameters from the GET request
    ### and returns the JSON form of the questionnaire requested 
    def load(self, query):
        connect_str = self._get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            #kwargs = {param : value}
            if 'uid' in query.keys():
                retrieved_questionnaire = session.query(Questionnaire).filter_by(**query).one()
                retrieved_json = retrieved_questionnaire._to_json()
            else:
                logging.info('---start query----')
                start_time = time.time()
                retrieved_questionnaires = session.query(Questionnaire).filter_by(**query).all()
                logging.info((time.time() - start_time))
                logging.info('---end query----')
                retrieved_json = []
                for ques in retrieved_questionnaires:
                    logging.info('---start tojson----')
                    start_time = time.time()
                    json_dict = ques._to_json()
                    logging.info((time.time() - start_time))
                    logging.info('----end tojson---')
                    retrieved_json.append(json_dict)
                retrieved_json = json.dumps(retrieved_json, indent=4)
            session.close()
            return retrieved_json
        except Exception as e:
            return str(e)

    def delete(self, uid):
        connect_str = self._get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            session.query(QuestionnaireItem).filter(QuestionnaireItem.quid==uid).delete()
            session.query(Questionnaire).filter(Questionnaire.uid==uid).delete()
            session.commit()
            session.close()
            return True
        except Exception as e:
            return e


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
        result = OrderedDict()
        start_time = time.time()     
        mapper = inspect(self)
        #logging.info("--- inspection time %s seconds ---" % (time.time() - start_time))
        for attribute in mapper.attrs:
            sstart_time = time.time()        
            key = attribute.key
            if attribute.value == None or key == "uid":
                continue
            if key == "item":
                start_time = time.time()
                result["item"] = self._build_item_list(attribute.value)
            elif key == "text":
                result["text"] = json.loads(getattr(self, key))
            elif key == "code":
                code_list = []
                for entry in attribute.value:
                    code_list.append(entry.to_dict())
                if len(code_list) > 0:
                    result[key] = code_list
            else:
                result[key] = getattr(self, key)
            #logging.info('--attribute here is %s--' % key)
            #logging.info("--- time for is %s seconds ---" % (time.time() - sstart_time))
        return result
   
   
   ### return the Questionnaire in a JSON format
    def _to_json(self):
        return json.dumps(self._to_dict(), indent=4)

    
    ### Return the list of questionnaire items 
    ### in json format of nested dicts
    ### to be returned 
    def _build_item_list(self, list_of_items):

        start_time = time.time()
        list_of_dicts = self._item_to_dict(list_of_items)
        #logging.info("--- building dicts takes %s seconds ---" % (time.time() - start_time))
        parent_list = []
        nesting_check = 0

        for entry in list_of_dicts:
            if entry["parent_id"] != None:
                nesting_check = 1
            else:
                parent_list.append(entry)
            entry["item"] = []
        start_time = time.time()
        while (nesting_check == 1):
            nesting_check = 0
            for item1 in list_of_dicts:
                for item2 in list_of_dicts:
                    if item1["parent_id"] == item2["linkId"] and item1["parent_id"] is not None:
                        item1["parent_id"] = None
                        item2["item"].append(item1)
                        nesting_check = 1
        #logging.info("--- building list nesting loops is %s seconds ---" % (time.time() - start_time))

        for entry in list_of_dicts:
            del entry["parent_id"]
            if len(entry["item"]) == 0:
                del entry["item"]
        return parent_list

    ### create the connection string for the database
    ### which will eventually take in an authorised token
    def _get_conn_string(self):
        # server = "tcp:fhir-questionnaire-server.database.windows.net"
        # database = "questionnaire-database"
        # username = "bencharlton"
        # password = "Benazure123"
        # driver = '{ODBC Driver 17 for SQL Server}'
        #os.environ["SQL_CONNECTION_STRING"] 
        odbc_str = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:questionnaire-sql-server.database.windows.net,1433;Database=questionnaire-database;Uid=bencharlton;Pwd=Bensql123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        return connect_str

        #os.environ[ODBC_CONNECTION_STRING]

    ### helper function to create the list of item dicts
    ### that gets processed to produce the final list
    @staticmethod
    def _item_to_dict(item_list):
        dict_list = []
        for item in item_list:
            start = time.time()
            dict_to_add = item.to_dict()
            logging.info("--- each dict takes %s seconds ---" % (time.time() - start))
            dict_list.append(dict_to_add)
        return dict_list

##################################################################################################################################
##################################################################################################################################

class QuestionnaireItemInitial(BaseModel,object):
    
    __tablename__ = "QuestionnaireItemInitial"
    id = Column(Integer, primary_key=True)
    iid = Column(Integer, ForeignKey('QuestionnaireItem.id', ondelete="cascade"))
    valueBoolean = Column(Boolean)
    valueDecimal = Column(Float)
    valueInteger = Column(Integer)
    valueDate = Column(Date)
    valueDateTime = Column(DateTime)
    valueString = Column(String)
    valueCoding = Column(String)
    
    def __init__(self):
        self.id = None
        self.valueBoolean = None
        self.valueDecimal = None
        self.valueInteger = None
        self.valueDate = None
        self.valueDateTime = None
        self.valueString = None
        self.valueCoding =  None

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "iid" or key == "id":
                pass
            else:
                if getattr(self, key) is not None:
                    if key == "valueCoding":
                        result[key] = json.loads(getattr(self, key))
                    else:
                        result[key] =  getattr(self, key)
        return result

    def update_with_dict(self, json_dict):
        for key in json_dict:
            if key == "valueCoding":
                setattr(self, key, json.dumps(json_dict[key]))      
            else:
                setattr(self, key, json_dict[key])      
        return
    
    def _save(self, session):
        session.add(self)
        return


##################################################################################################################################
##################################################################################################################################

class QuestionnaireItemAnswerOption(BaseModel, object):
    __tablename__ = "QuestionnaireItemAnswerOption"
    id = Column(Integer, primary_key=True)
    iid = Column(Integer, ForeignKey('QuestionnaireItem.id', ondelete="cascade"))
    valueInteger = Column(Integer)
    valueDate = Column(Date)
    valueTime = Column(DateTime)
    valueString = Column(String)
    valueCoding = Column(String)
    initialSelected = Column(Boolean)

    def __init__(self):
        self.id = None
        self.valueInteger = None
        self.valueDate = None
        self.valueDateTime = None
        self.valueString = None
        self.valueCoding = None
        self.initialSelected = None

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "iid" or key == "id":
                pass
            else:
                if getattr(self, key) is not None:
                    if key == "valueCoding":
                        result[key] = json.loads(getattr(self, key))
                    else:
                        result[key] =  getattr(self, key)
        return result

    def update_with_dict(self, json_dict):
        for key in json_dict:
            if key == "valueCoding":
                setattr(self, key, json.dumps(json_dict[key]))      
            else:
                setattr(self, key, json_dict[key])       
        return

    def _save(self, session):
        session.add(self)
        return


##################################################################################################################################
##################################################################################################################################

class Coding(BaseModel, object):
    
    __tablename__ = "Coding"
    id = Column(Integer, primary_key=True)
    quid = Column(String(100), ForeignKey('Questionnaire.uid', ondelete="cascade"))
    iid = Column(Integer, ForeignKey('QuestionnaireItem.id', ondelete="cascade"))
    system = Column(String)
    version = Column(String)
    code = Column(String)
    display = Column(String)
    userSelected = Column(Boolean)
    
    def __init__(self):
        
        self.system = None
        self.version = None
        self.code = None
        self.display = None
        self.userSelected = None

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "id" or key == "quid" or key == "iid":
                pass
            else:
                if getattr(self, key) is not None:
                    result[key] = getattr(self, key)
        return result

    def update_with_dict(self, json_dict):
        for key in json_dict:
            setattr(self, key, json_dict[key])
        return

    def _save(self, session):
        session.add(self)
        return


##################################################################################################################################
##################################################################################################################################

class QuestionnaireItemEnableWhen(BaseModel,object):
    __tablename__ = "QuestionnaireItemEnableWhen"
    id = Column(Integer, primary_key=True)
    iid = Column(Integer, ForeignKey('QuestionnaireItem.id', ondelete="cascade"))
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

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        #logging.info('--- for enable to dict---')
        for attribute in mapper.attrs:
            start = time.time()
            key = attribute.key
            if key == "iid" or key == "id":
                pass
            elif key == "answerCoding":
                result[key] = json.loads(attribute.value)
            else:
                if getattr(self, key) is not None:
                    result[key] =  getattr(self, key)
        #logging.info("--- takes %s seconds ---" % (time.time() - start))
        return result

    def update_with_dict(self, json_dict):
        for key in json_dict:
            if key == "answerCoding":
                self.answerCoding = json.dumps(json_dict[key])
            else:
                setattr(self, key, json_dict[key])      
        return
    
    def _save(self, session):
        session.add(self)
        return

##################################################################################################################################
##################################################################################################################################

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
            else:
                setattr(self, key, item_dict[key])
                
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
                    if isinstance(getattr(self, key), list):
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