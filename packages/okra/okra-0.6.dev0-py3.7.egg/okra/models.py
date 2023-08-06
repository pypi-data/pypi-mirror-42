""" SQL Database Models 

This is the database schema used for accessing the SQL database.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (Table, Column, Integer, String, MetaData, Numeric,
                        ForeignKey, DateTime, create_engine)

Base = declarative_base()

class Cookie(Base):
    __tablename__ = 'cookies'

    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

class CommitMeta(Base):

    __tablename__ = 'commit_meta'

    commit_hash = Column('commit_hash', String(40), primary_key=True)
    owner_name = Column('owner_name', String(100), nullable=False)
    project_name = Column('project_name', String(150), nullable=False)
    

class DataAccessLayer(object):

    def __init__(self, conn_string):
        self.engine = None
        self.session = None
        self.conn_string = conn_string

    def connect(self):
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
