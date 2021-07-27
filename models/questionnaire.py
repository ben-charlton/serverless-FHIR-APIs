from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
import urllib
import pyodbc
import json
from collections import OrderedDict
from functools import cmp_to_key
from questionnaireitem import QuestionnaireItem
from coding import Coding

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
    id = Column(String(450), primary_key=True) #450 needed because wont let primary key be max varchar
    text = Column(String)
    url = Column(String)
    name = Column(String)
    title = Column(String)
    status = Column(String)
    date = Column(DateTime)
    publisher = Column(String)
    description = Column(String)
    purpose = Column(String)
    copyright = Column(String)
    code = relationship("Coding", lazy=True)
    item = relationship('QuestionnaireItem', back_populates="questionnaire", lazy = True)

    def __init__(self):
        self.resourceType = "Questionnaire"
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
            #elif key == "text":
            #    text_string = json.dumps(json_dict[key], indent=4)
            #    setattr(self, key, json_dict[key])
            elif key == "item":
                items_list = json_dict[key]
                for item_dict in items_list:
                    new_item = QuestionnaireItem()
                    new_item.update_with_dict(item_dict, json_dict["id"], None)
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
            engine = create_engine(connect_str)
            BaseModel.metadata.create_all(engine)
            session = Session(engine)
            session.begin()
            session.add(self)
            self._save_child_elements(session)
            session.commit()
            session.close()
            return True
        except:
            return False


    ### Takes in the query parameters from the GET request
    ### and returns the JSON form of the questionnaire requested 
    def load(self, param, value):
        connect_str = self._get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            kwargs = {param : value}
            retrieved_questionnaire = session.query(Questionnaire).filter_by(**kwargs).one()
            retrieved_json = retrieved_questionnaire._to_json()
            session.close()
            return retrieved_json
        except:
            return None

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
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "item":
                result["item"] = self._build_item_list(attribute.value)
            else:
                result[key] = getattr(self, key)
        return result


    ### Return the list of questionnaire items 
    ### in json format of nested dicts
    ### to be returned 
    def _build_item_list(self, list_of_items):
        
        list_of_dicts = self._item_to_dict(list_of_items)
        parent_list = []
        nesting_check = 0
        for entry in list_of_dicts:
            if entry["parentId"] != None:
                nesting_check = 1
            else:
                parent_list.append(entry)
            entry["item"] = []

        while (nesting_check == 1):
            nesting_check = 0
            for item1 in list_of_dicts:
                for item2 in list_of_dicts:
                    if item1["parentId"] == item2["linkId"] and item1["parentId"] is not None:
                        item1["parentId"] = None
                        item2["item"].append(item1)
                        nesting_check = 1

        for entry in list_of_dicts:
            del entry["parentId"]
            if len(entry["item"]) == 0:
                del entry["item"]

        return parent_list


    ### return the Questionnaire in a JSON format
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
        odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        return connect_str

    ### helper function to create the list of item dicts
    ### that gets processed to produce the final list
    def _item_to_dict(self, item_list):
        dict_list = []
        for item in item_list:
            dict_to_add = item.to_dict()
            dict_list.append(dict_to_add)
        return dict_list






