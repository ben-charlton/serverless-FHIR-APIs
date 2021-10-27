from sqlalchemy import Column, Integer, String, create_engine, Boolean, Float, Date, DateTime, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
import urllib
import pyodbc
import uuid
import os
from models.base import BaseModel

### USER CLASS DEFINITION
class User(BaseModel):

    ### The ORM mapping for the object 
    __tablename__ = "User"
    user_id = Column(String(200))
    token = Column(String(200), primary_key=True) 

    def __init__(self):
        self.user_id = uuid.uuid4().hex
        self.token = None


    def load(self, token):
        connect_str = self._get_conn_string()
        try:
            engine = create_engine(connect_str)
            session = Session(engine)
            user = session.query(User).filter_by(token=token).first()
            if (user is not None):
                return user.user_id
            else:
                raise Exception("User does not exist for given token")
        except Exception as e:
            raise Exception(str(e))


    def save(self, token):
        self.token = token
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
        except Exception as e:
            raise Exception(str(e))


    def _get_conn_string(self):
        odbc_str = os.environ["SQL_CONNECTION_STRING"] 
        connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)
        return connect_str
    