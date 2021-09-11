from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict
import json
import urllib
import uuid
import logging
import time
import os

BaseModel = declarative_base(name='BaseModel')

### QUESTIONNAIRERESPONSE CLASS DEFINITION
### This is the ORM mapped class that is used to create
### questionnaireResponse objects from a given JSON body (POST),
### and stored in the SQL database to be retrieved (GET)
class QuestionnaireResponse(BaseModel, object):

    ### The ORM mapping for the object 
    ### This creates the table in the database (once only)
    ### and sets up the mapping from object->database
    __tablename__ = "QuestionnaireResponse"
    resourceType = Column(String)
    uid = Column(String(100), primary_key=True)
    id = Column(String) 
    text = Column(String)
    identifier = Column(String)
    #basedOn = relationship("Reference")
    #partOf = relationship("Reference")
    questionnaire = Column(String)
    status = Column(String)
    subject = Column(String)
    encounter = Column(String)
    authored = Column(String)
    author = Column(String)
    source = Column(String)
    item = relationship('QuestionnaireResponseItem',cascade='delete', back_populates="questionnaireResponse", lazy = True)
    contained = relationship("Contained", cascade='delete', lazy=True, back_populates="response")
    
    def __init__(self):

        self.resourceType = "QuestionnaireResponse" 
        self.uid = uuid.uuid4().hex
        self.id = None
        self.text = None
        self.contained = []
        self.identifier = None
        #self.basedOn = None
        #self.partOf = None
        self.questionnaire = None
        self.status = None  
        self.subject = None
        self.encounter = None
        self.authored = None
        self.author = None
        self.source = None
        self.item = []


    ### This function takes in the posted JSON from the request
    ### and fills the newly created object with the data,
    ### setting each attribute to the respective field in the JSON
    def update_with_json(self, json_dict):
        for key in json_dict:
            if key == "identifier" or key == "questionnaire" or key == "subject" or key == "encounter" or key == "source" or key == "author" or key == "text":
                setattr(self, key, json.dumps(json_dict[key], indent=4))
            elif key == "item":
                items_list = json_dict[key]
                for item_dict in items_list:
                    new_item = QuestionnaireResponseItem()
                    new_item.update_with_dict(item_dict, self.uid, None)
                    self.item.append(new_item)
            elif key == "contained":
                contained_list = json_dict[key]
                for entry in contained_list:
                    contained_item = Contained()
                    contained_item.update(self.uid, entry)
                    self.contained.append(contained_item)
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
            return str(e)


    ### Takes in the query parameters from the GET request
    ### and returns the JSON form of the questionnaire requested 
    def load(self, query):
        connect_str = self._get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            #kwargs = {param : value}
            if 'uid' in query.keys():
                retrieved_response = session.query(QuestionnaireResponse).filter_by(**query).one()
                retrieved_json = retrieved_response._to_json()
            else:
                logging.info('---start query----')
                start_time = time.time()
                retrieved_responses = session.query(QuestionnaireResponse).filter_by(**query).all()
                logging.info((time.time() - start_time))
                logging.info('---end query----')
                retrieved_json = []
                for res in retrieved_responses:
                    logging.info('---start tojson----')
                    start_time = time.time()
                    json_dict = res._to_json()
                    logging.info((time.time() - start_time))
                    logging.info('----end tojson---')
                    retrieved_json.append(json_dict)
                retrieved_json = json.dumps(retrieved_json)
            session.close()
            return retrieved_json
        except Exception as e:
            return str(e)

    def delete(self, uid):
        connect_str = self._get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            res = session.query(QuestionnaireResponse).filter(QuestionnaireResponse.uid==uid)
            session.delete(res)
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
        for contained in self.contained:
            contained._save(session)
        return

    ### converts the Questionnaire object into a dictionary 
    ### that can then be JSONified and returned through a (GET)
    def _to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if attribute.value == None:
                continue
            if key == "item":
                result["item"] = json.loads(self._build_item_list(attribute.value))
            elif key == "identifier" or key == "questionnaire" or key == "subject" or key == "encounter" or key == "source" or key == "author" or key == "text":
                result[key] = json.loads(getattr(self, key))
            elif key == "contained":
                cont_list = []
                for entry in attribute.value:
                    cont_list.append(entry.to_dict())
                if len(cont_list) > 0:
                    result[key] = cont_list
            else:
                result[key] = getattr(self, key)
        return result


    ### Return the list of questionnaireResponseItems 
    ### in json format of nested dicts to be returned 
    ### and placed into the response json
    def _build_item_list(self, list_of_items):
    
        item_dicts = self._items_to_dicts(list_of_items)
        answer_dicts = self._get_answer_dicts(list_of_items)
        parent_list, nesting_check = self._create_helper_fields(item_dicts, answer_dicts)

        while (nesting_check == 1):
            nesting_check = 0
            for item1 in item_dicts:
                for item2 in item_dicts:
                    if item2["answer_id"] != None:
                        for answer in answer_dicts:
                            if (item2["parent_id"] == answer["item_id"]) and item2["answer_id"] == answer["answer_counter"]:
                                answer["item"].append(item2)
                                item2["answer_id"] = None
                                item2["parent_id"] = None
                    if item1["parent_id"] == item2["linkId"] and item1["parent_id"] is not None:
                        item1["parent_id"] = None
                        item2["item"].append(item1)
                        nesting_check = 1
                for answer in answer_dicts:
                    if answer["item_id"] == item1["linkId"]:
                        item1["answer"].append(answer)
                        answer["item_id"] = None

        self._delete_unnecessary_fields(item_dicts, answer_dicts)
        return json.dumps(parent_list, indent=4)

   ### return the QuestionnaireResponse in a JSON format
    def _to_json(self):
        return json.dumps(self._to_dict(), indent=4)
    
    
    ### create the connection string for the database
    ### which will eventually take in an authorised token
    def _get_conn_string(self):
        server = "tcp:fhir-questionnaire-server.database.windows.net"
        database = "questionnaire-database"
        username = "bencharlton"
        password = "Benazure123"
        driver = '{ODBC Driver 17 for SQL Server}'
        #os.environ["SQL_CONNECTION_STRING"]
        odbc_str = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:questionnaire-sql-server.database.windows.net,1433;Database=questionnaire-database;Uid=bencharlton;Pwd=Bensql123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        return connect_str


    @staticmethod
    def _create_helper_fields(item_dicts, answer_dicts):
        parent_list = []
        nesting_check = 0
        for entry in item_dicts:
            if entry["parent_id"] != None:
                nesting_check = 1
            else:
                parent_list.append(entry)
            entry["item"] = []
            entry["answer"] = []
        for entry in answer_dicts:
            entry["item"] = []
        return parent_list, nesting_check

    @staticmethod
    def _delete_unnecessary_fields(item_dicts, answer_dicts):
        for entry in item_dicts:
            del entry["parent_id"]
            del entry["answer_id"]
            if len(entry["item"]) == 0:
                del entry["item"]
            if len(entry["answer"]) == 0:
                del entry["answer"]
        for entry in answer_dicts:
            del entry["item_id"]
            del entry["answer_counter"]
            if len(entry["item"]) == 0:
                del entry["item"]
        return

    @staticmethod
    def _items_to_dicts(item_list):
        dict_list = []
        for item in item_list:
            dict_to_add = item.to_dict()
            dict_list.append(dict_to_add)
        return dict_list

    @staticmethod
    def _get_answer_dicts(list_of_items):
        answer_dict_list = []
        for item in list_of_items:
            mapper = inspect(item)
            for attribute in mapper.attrs:
                if attribute.key == "answer":
                    for answer in attribute.value:
                        answer_dict_list.append(answer.to_dict())
        return answer_dict_list

#########################################################################################################################
#########################################################################################################################
class Contained(BaseModel, object):
    __tablename__ = "Contained"
    id = Column(Integer, primary_key=True)
    response_id = Column(String(100), ForeignKey('QuestionnaireResponse.uid')) 
    response = relationship("QuestionnaireResponse", back_populates="contained")
    string = Column(String)

    def __init__(self):
        self.response_id = None
        self.string = None
    
    def update(self, response_id, resource_dict):
        self.response_id = response_id
        self.string = json.dumps(resource_dict, indent=4)
        return

    def to_dict(self):
        return json.loads(self.string)

    def _save(self, session):
        session.add(self)
        return

#########################################################################################################################
#########################################################################################################################
class QuestionnaireResponseItemAnswer(BaseModel, object):
    __tablename__ = "QuestionnaireResponseItemAnswer"
    id = Column(Integer, primary_key=True)
    item_FK = Column(Integer, ForeignKey('QuestionnaireResponseItem.id'))
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
                setattr(self, key, json_dict[key])
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

#########################################################################################################################
#########################################################################################################################

class QuestionnaireResponseItem(BaseModel, object):
    __tablename__ = "QuestionnaireResponseItem"
    id = Column(Integer, primary_key=True)
    response_id = Column(String(100), ForeignKey('QuestionnaireResponse.uid'))
    questionnaireResponse = relationship("QuestionnaireResponse", cascade='delete', back_populates="item", foreign_keys=[response_id])
    parent_id = Column(String)
    linkId = Column(String)
    definition = Column(String)
    text = Column(String)
    answer_id = Column(Integer)
    answer = relationship("QuestionnaireResponseItemAnswer", cascade='delete')


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
                setattr(self, key, item_dict[key])
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

#########################################################################################################################
#########################################################################################################################