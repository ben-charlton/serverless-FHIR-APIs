from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from collections import OrderedDict

BaseModel = declarative_base(name='BaseModel')
class QuestionnaireResponse(BaseModel, object):
    __tablename__ = "QuestionnaireResponse"
    resourceType = Column(String)
    id = Column(String(450), primary_key=True) 
    text = Column(String)
    identifier = Column(String)
    basedOn = relationship("Reference")
    partOf = relationship("Reference")
    questionnaire = Column(String)
    status = Column(String)
    subject = Column(String)
    encounter = Column(String)
    authored = Column(DateTime)
    author = Column(String)
    source = Column(String)
    item = relationship('QuestionnaireResponseItem', back_populates="questionnaireResponse", lazy = True)
    
    def __init__(self):

        self.resourceType = "QuestionnaireResponse" 
        self.text = None
        self.identifier = None
        self.basedOn = None
        self.partOf = None
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
            if key == "item":
                items_list = json_dict[key]
                for item_dict in items_list:
                    new_item = QuestionnaireResponseItem()
                    new_item.update_with_dict(item_dict, json_dict["id"], None)
                    self.item.append(new_item)
            else:
                setattr(self, key, json_dict[key])
        return

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
            item._save(session)
        return

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

    def _item_to_dict(self, item_list):
        dict_list = []
        for item in item_list:
            dict_to_add = item.to_dict()
            dict_list.append(dict_to_add)
        return dict_list