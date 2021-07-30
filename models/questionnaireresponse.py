from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict
import json
import urllib

BaseModel = declarative_base(name='BaseModel')

class QuestionnaireResponse(BaseModel, object):
    __tablename__ = "QuestionnaireResponse"
    resourceType = Column(String)
    id = Column(String(450), primary_key=True) 
    text = Column(String)
    identifier = Column(String)
    #basedOn = relationship("Reference")
    #partOf = relationship("Reference")
    questionnaire = Column(String)
    status = Column(String)
    subject = Column(String)
    encounter = Column(String)
    authored = Column(DateTime)
    author = Column(String)
    source = Column(String)
    item = relationship('QuestionnaireResponseItem', back_populates="questionnaireResponse", lazy = True)
    contained = relationship("Contained",lazy=True)
    
    def __init__(self):

        self.resourceType = "QuestionnaireResponse" 
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

    def update_with_json(self, json_dict):
        for key in json_dict:
            if key == "identifier" or key == "questionnaire" or key == "subject" or key == "encounter" or key == "source" or key == "author":
                setattr(self, key, json.dumps(json_dict[key], indent=4))
            elif key == "item":
                items_list = json_dict[key]
                for item_dict in items_list:
                    new_item = QuestionnaireResponseItem()
                    new_item.update_with_dict(item_dict, json_dict["id"], False, None)
                    self.item.append(new_item)
            elif key == "contained":
                contained_list = json_dict[key]
                for entry in contained_list:
                    contained_item = Contained(json_dict["id"], entry)
                    self.contained.append(contained_item)
            else:
                setattr(self, key, json_dict[key])
        return

    def save(self):
        connect_str = self._get_conn_string()
        try: 
            engine = create_engine(connect_str)#, echo=True)
            try:
                BaseModel.metadata.create_all(engine)
            except Exception as e:
                print(str(e))
            print('here10')
            session = Session(engine)
            print('here11')
            session.begin()
            print('here12')
            try:
                session.add(self)
                self._save_child_elements(session)
            except Exception as e:
                print(str(e))
            print('here13')
            try:
                session.commit()
            except Exception as e:
                print(str(e))
            session.close()
            return True
        except Exception as e:
            print(str(e))
            return False


    def load(self, param, value):
        connect_str = self._get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            kwargs = {param : value}
            questionnaire_response = session.query(QuestionnaireResponse).filter_by(**kwargs).one()
            retrieved_json = questionnaire_response._to_json()
            session.close()
            return retrieved_json
        except:
            return None

    def _save_child_elements(self, session):
        for item in self.item:
            print("---item here----")
            print(item.linkId)
            item._save(session)
        print('here7.5')
        for contained in self.contained:
            contained._save(session)
        print('here8')
        return

    def _to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if attribute.value == None:
                continue
            if key == "item":
                result["item"] = self._build_item_list(attribute.value)
            elif key == "identifier" or key == "questionnaire" or key == "subject" or key == "encounter" or key == "source" or key == "author":
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


    def _build_item_list(self, list_of_items):
    
        item_dicts = self._items_to_dicts(list_of_items)
        answer_dicts = self._get_answer_dicts_from_items(list_of_items)
        return
        # parent_list = []
        # nesting_check = 0
        # for entry in item_dicts:
        #     if entry["parent_id"] != None:
        #         nesting_check = 1
        #     else:
        #         parent_list.append(entry)
        #     entry["item"] = []

        # while (nesting_check == 1):
        #     nesting_check = 0
        #     for item1 in item_dicts:
        #         for item2 in item_dicts:
        #             if item1["parent_id"] == item2["linkId"] and item1["parent_id"] is not None:
        #                 item1["parent_id"] = None
        #                 item2["item"].append(item1)
        #                 nesting_check = 1

        # for entry in item_dicts:
        #     del entry["parent_id"]
        #     if len(entry["item"]) == 0:
        #         del entry["item"]

        # return parent_list

    def _to_json(self):
        return json.dumps(self._to_dict(), indent=4)


    def _get_conn_string(self):
        server = "tcp:fhir-questionnaire-server.database.windows.net"
        database = "questionnaire-database"
        username = "bencharlton"
        password = "Benazure123"
        driver = '{ODBC Driver 17 for SQL Server}'
        odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        return connect_str

    def _items_to_dicts(self, item_list):
        dict_list = []
        for item in item_list:
            dict_to_add = item.to_dict()
            dict_list.append(dict_to_add)
        return dict_list

    def _get_answer_dicts_from_items(self, list_of_items):
        answer_dict_list = []
        for item in list_of_items:
            result = OrderedDict()
            mapper = inspect(self)
            for attribute in mapper.attrs:
                if attribute.key == "answer":
                    print('---item looking at----')
                    print(item.id)
                    print('-----items answers------')
                    print(attribute.value)
        return answer_dict_list

#########################################################################################################################
#########################################################################################################################
class Contained(BaseModel, object):
    __tablename__ = "Contained"
    id = Column(Integer, primary_key=True)
    response_id = Column(String(450), ForeignKey('QuestionnaireResponse.id')) 
    response = relationship("QuestionnaireResponse", back_populates="contained")
    string = Column(String)

    def __init__(self, response_id, resource_dict):
        self.response_id = response_id
        self.string = json.dumps(resource_dict, indent=4)

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
    item_id = Column(Integer, ForeignKey('QuestionnaireResponseItem.id'))
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

    def update_with_dict(self, item_dict, response_id):
        for key in item_dict:
            if key == "valueAttachment" or key == "valueCoding" or key == "valueQuantity" or key == "valueReference":
                setattr(self, key, json.dumps(item_dict[key], indent=4))
            elif key == "item":
                items_list = item_dict[key]
                for single_item_dict in items_list:
                    new_item = QuestionnaireResponseItem()
                    new_item.update_with_dict(single_item_dict, response_id, True, single_item_dict["linkId"])
                    self.item.append(new_item)  
            else:
                setattr(self, key, item_dict[key])
        return

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if attribute.value == None:
                continue
            if key == "item_id" or key == "id":
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
        for answer in self.answer:
            answer._save(session)
        return

#########################################################################################################################
#########################################################################################################################

class QuestionnaireResponseItem(BaseModel, object):
    __tablename__ = "QuestionnaireResponseItem"
    id = Column(Integer, primary_key=True)
    response_id = Column(String(450), ForeignKey('QuestionnaireResponse.id'))
    questionnaireResponse = relationship("QuestionnaireResponse", back_populates="item", foreign_keys=[response_id])
    parent_id = Column(String)
    linkId = Column(String)
    definition = Column(String)
    text = Column(String)
    is_answer = Column(Boolean)
    answer_id = Column(Integer, ForeignKey('QuestionnaireResponseItemAnswer.id'))
    answer = relationship("QuestionnaireResponseItemAnswer", foreign_keys=[answer_id])


    def __init__(self):
       
        self.linkId = None
        self.definition = None
        self.text = None
        self.answer = []
        self.item = []
        self.response_id = None
        self.parent_id = None
        self.answer_id = None

    def update_with_dict(self, item_dict, response_id, is_answer, parent_id=None):
        self.response_id = response_id
        self.parent_id = parent_id
        self.is_answer = is_answer
        for key in item_dict:
            if key == "answer":
                answer_list = item_dict[key]
                for entry in answer_list:
                    answer = QuestionnaireResponseItemAnswer()
                    answer.update_with_dict(entry, response_id)
                    self.answer.append(answer)
            elif key == "item":
                items_list = item_dict[key]
                for single_item_dict in items_list:
                    new_item = QuestionnaireResponseItem()
                    new_item.update_with_dict(single_item_dict, response_id, False, item_dict["linkId"])
                    self.item.append(new_item)  
            else:
                setattr(self, key, item_dict[key])
        return

    def to_dict(self):
        result = OrderedDict()
        mapper = inspect(self)
        for attribute in mapper.attrs:
            key = attribute.key
            if key == "questionnaireResponse" or key == "id" or key == "answer":
                pass
            else:
                result[key] = getattr(self, key)
        return result

    def _save(self, session):
        session.add(self)
        print('here???/')
        for item in self.item:
            item._save(session)
        for answer in self.answer:
            answer._save(session)
        return

#########################################################################################################################
#########################################################################################################################