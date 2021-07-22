from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
import urllib
import pyodbc
import json
from collections import OrderedDict
from functools import cmp_to_key

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
    id = Column(String(450), primary_key=True) #450 needed because wont let primary key be max varchar
    name = Column(String)
    url = Column(String)
    title = Column(String)
    items = relationship('QuestionnaireItem', back_populates="questionnaire", lazy = True)
    
    def __init__(self):
        self.id = None 
        self.name = None
        self.url = None
        self.title = None
        # self.items stores the 'outer' items in each questionnaire, 
        # i.e. the main items in the list with no nesting (integer linkIds)
        # this is only really useful when saving the object, can't access
        # this attribute when loading 
        self.items = [] 


    ### This function takes in the posted JSON from the request
    ### and fills the newly created object with the data,
    ### setting each attribute to the respective field in the JSON
    def update_with_json(self, json_dict):
        for key in json_dict:
            if key != "item":
                setattr(self, key, json_dict[key])
            elif key == "item":
                items_list = json_dict[key]
                for single_item_dict in items_list:
                    new_item = QuestionnaireItem()
                    # this then updates each 'outer' item with their respective nesting
                    new_item.update_with_dict(single_item_dict)
                    self.items.append(new_item)
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
        for item in self.items:
            item._save(session)
        return

    ### converts the Questionnaire object into a dictionary 
    ### that can then be JSONified and returned through a (GET)
    def _to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "items":
                result["item"] = self._build_item_list(attribute.value)
            else:
                result[key] = getattr(self, key)
        return result


    ### Return the list of questionnaire items 
    ### in json format of nested dicts
    ### to be returned 
    def _build_item_list(self, list_of_items):
        
        list_of_dicts = self._item_to_dict(list_of_items)

        for entry in list_of_dicts:
            entry["sortid"] = (entry["linkId"]).replace('.','')
            entry["item"] = []

        s_list = sorted(list_of_dicts, key=cmp_to_key(self.compare_item_ids))

        maxNesting = 0
        for entry in list_of_dicts:
            nesting = len(entry["sortid"])
            if nesting > maxNesting:
                maxNesting = nesting

        while maxNesting > 1:
            itemIndex = 0
            while itemIndex < len(s_list):
                if ("sortid" in s_list[itemIndex]) and (len(s_list[itemIndex]["sortid"]) == maxNesting):
                    innerIndex = 0
                    while innerIndex < len(s_list):
                        if ("sortid" in s_list[innerIndex]) and (len(s_list[innerIndex]["sortid"]) == maxNesting -1) :
                            s1 = s_list[innerIndex]["sortid"]
                            s2 = s_list[itemIndex]["sortid"][:-1]
                            if (s1 == s2) :
                                del s_list[itemIndex]["sortid"]
                                s_list[innerIndex]["item"].append(s_list[itemIndex])
                                break
                        innerIndex += 1
                itemIndex +=1
            maxNesting -= 1

        s_list = [x for x in s_list if "sortid" in x]

        for entry in s_list:
            del entry["sortid"]
            self.removeInnermostItem(entry)
        
        return s_list


    ### Helper function to remove the excess
    ### 'item' field in the innermost item dict
    def removeInnermostItem(self, currentItem):
        if "item" in currentItem:
            if len(currentItem["item"]) == 0:
                del currentItem["item"]
            else:
                for innerItem in currentItem["item"]:
                    self.removeInnermostItem(innerItem)


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
    
    ### This method is an internal method used by build_list_items
    ### to sort items by linkId order, in order to create the 
    ### nested list of item dicts to return the JSON for a GET request
    @staticmethod
    def compare_item_ids(item1, item2):
        if item1["linkId"] < item2["linkId"]:
            return -1
        elif item1["linkId"] > item2["linkId"]:
            return 1
        else:
            return 0

    ### helper function to create the list of item dicts
    ### that gets processed to produce the final list
    @staticmethod
    def _item_to_dict(item_list):
        dict_list = []
        for item in item_list:
            dict_to_add = item.to_dict()
            dict_list.append(dict_to_add)
        return dict_list


class QuestionnaireItem(BaseModel):
    __tablename__ = "QuestionnaireItem"
    dummyCol = Column(Integer, primary_key=True)
    questionnaire = relationship("Questionnaire", back_populates="items")
    linkId = Column(String)
    questionnaire_id = Column(String(450), ForeignKey('Questionnaire.id'))
    text = Column(String)
    #prefix = Column(String)
    #enable_when = relationship("QuestionnaireItemEnableWhen", back_populates="item", uselist=False)

    def __init__(self):
        self.linkId = None
        self.questionnaire_id = None
        self.text = None
        # again, self.items here is used to save off the elements
        # into the table in the database
        self.items = []
        #self.enable_when = None # list represented in JSON as Dict
        #self.prefix = None

    def update_with_dict(self, item_dict):
        for key in item_dict:
            if key != "item":
                setattr(self, key, item_dict[key])
            elif key == "item":
                items_list = item_dict[key]
                for single_item_dict in items_list:
                    new_item = QuestionnaireItem()
                    new_item.update_with_dict(single_item_dict)
                    self.items.append(new_item) 
        return

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "questionnaire" or key == "questionnaire_id" or key == "dummyCol":
                pass
                #result["item"] = self._build_item_list(attribute.value)
            else:
                result[key] = getattr(self, key)
        return result


    def _save(self, session):
        session.add(self)
        for item in self.items:
            item._save(session)
        return


# class QuestionnaireItemEnableWhen(BaseModel):
#     __tablename__ = "QuestionnaireItemEnableWhen"
#     id = Column(Integer)
#     item = relationship("QuestionnaireItem", back_populates="enable_when")
#     question = Column(String)
#     operator = Column(String)
    # answerBoolean = Column(Boolean)
    # answerDecimal = Column(Float)
    # answerInteger = Column(Integer)
    # answerDate = Column(Date)
    # answerDateTime = Column(DateTime)
    # answerString = Column(String)

#     def __init__(self):
#         self.id = None
#         self.item = None
#         self.question = None
#         self.operator = None

# class QuestionnaireItemAnswerOption(BaseModel):
    # __tablename__ = "QuestionnaireItemAnswer"
    # id = Column(Integer)
    # valueInteger = Column(Integer)
    # valueDate = Column(Date)
    # valueTime = Column(DateTime)
    # valueString = Column(String)

    # def __init__(self):
    #     self.id = None
    #     self.valueInteger = None
    #     self.valueDate = None
    #     self.valueDateTime = None
    #     self.valueString = None

#class QuestionnaireItemInitial(BaseModel):
    
    # __tablename__ = "QuestionnaireItemAnswer"
    # id = Column(Integer)
    # valueBoolean = Column(Boolean)
    # valueDecimal = Column(Float)
    # valueInteger = Column(Integer)
    # valueDate = Column(Date)
    # valueDateTime = Column(DateTime)
    # valueString = Column(String)
    
    #def __init__(self):
    # self.id = None
    # self.valueBoolean = None
    # self.valueDecimal = None
    # self.valueInteger = None
    # self.valueDate = None
    # self.valueDateTime = None
    # self.valueString = None
