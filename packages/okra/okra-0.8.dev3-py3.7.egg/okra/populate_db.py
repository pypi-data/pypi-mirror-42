""" Populate SQL database. 

References:
  https://docs.sqlalchemy.org/en/latest/orm/tutorial.html
"""
import logging

from sqlalchemy.orm import Session

from okra.models import (Meta, Author, Contrib, CommitFile, Info,
                         DataAccessLayer)
                         

logger = logging.getLogger(__name__)


def insert_buffer(items: iter) -> bool:
    csession = Session()

    
    






