from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
import urllib
import pyodbc
import json
import jsonpickle
from sqlalchemy import inspect
#from encoder import QuestionnaireEncoder

BaseModel = declarative_base(name='BaseModel')

class Questionnaire(BaseModel, object):
    __tablename__ = "Questionnaire"
    id = Column(String(450), primary_key=True) #450 needed because wont let primary key be max varchar
    name = Column(String)
    url = Column(String)
    title = Column(String)
    #item = relationship('QuestionnaireItem', lazy = True)
    
    def __init__(self):
        self.id = None 
        self.name = None
        self.url = None
        self.title = None 
        #self.item = None # list of QuestionnaireItem items represented as dict in JSON

    def update_with_json(self, json_dict):
        for key in json_dict:
            setattr(self, key, json_dict[key])
        return
 

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        #return json.dumps(self.__dict__)
        #return jsonpickle.encode(self, unpicklable=False, make_refs=False)

    def to_json(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


    def save(self):
        connect_str = self.get_conn_string()
        try: 
            engine = create_engine(connect_str)
            BaseModel.metadata.create_all(engine)
            session = Session(engine)
            session.begin()
            session.add(self)
            session.commit()
            session.close()
            return True
        except:
            return False
    

    def load(self, param, value):
        connect_str = self.get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            kwargs = {param : value}
            retrieved_questionnaire = session.query(Questionnaire).filter_by(**kwargs).one()
            retrieved_dict = retrieved_questionnaire.to_json()
            retrieved_json = json.dumps(retrieved_dict, indent = 4) 
            return retrieved_json
        except:
            return None

    def get_conn_string(self):
        server = "tcp:fhir-questionnaire-server.database.windows.net"
        database = "questionnaire-database"
        username = "bencharlton"
        password = "Benazure123"
        driver = '{ODBC Driver 17 for SQL Server}'
        odbc_str = 'DRIVER='+driver+';SERVER='+server+';PORT=1433;UID='+username+';DATABASE='+ database + ';PWD='+ password
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        return connect_str

# class QuestionnaireItem(BaseModel):
#     __tablename__ = "QuestionnaireItem"
#     id = Column(String, primary_key=True)
#     questionnaire_id = Column(Integer, ForeignKey('Questionnaire.id'))
#     linkId = Column(String)
#     text = Column(String)
#     enable_when = relationship("QuestionnaireItemEnableWhen", back_populates="item", uselist=False)

    #def __init__(self):
        #self.id = None
#         self.questionnaire_id = None
#         self.linkId = None
#         self.text = None
        #self.enable_when = None # list represented in JSON as Dict
        #self.item = None # list of nested items represented in JSON as Dict - need to be just references to other item ids?


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
