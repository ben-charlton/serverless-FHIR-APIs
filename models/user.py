from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
import urllib
import pyodbc
import uuid
import os

BaseModel = declarative_base(name='BaseModel')

### USER CLASS DEFINITION
class User(BaseModel):

    ### The ORM mapping for the object 
    __tablename__ = "User"
    user_id = Column(String(100), primary_key=True)
    domain_name = Column(String) 

    def __init__(self):
        self.user_id = uuid.uuid4().hex
        #self.domain_name = None


    def verify(self, domain, id):
        connect_str = self._get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            #domain_name=domain,
            user = session.query(User).filter_by(user_id=id).first()
            if (user is not None):
                return True
            else: 
                return False
        except Exception as e:
            return str(e)


    # should take domain in future
    def save(self):
        connect_str = self._get_conn_string()
        try:
            return_uid = self.user_id
            engine = create_engine(connect_str)
            BaseModel.metadata.create_all(engine)
            session = Session(engine)
            session.begin()
            session.add(self)
            session.commit()
            session.close()
            return return_uid
        except Exception:
            return None


    def _get_conn_string(self):
        odbc_str = os.environ["SQL_CONNECTION_STRING"] 
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        return connect_str
    