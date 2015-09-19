#!/usr/bin/env python
# -*- coding:  utf-8 -*-

"""
Tasks
~~~~~~~~~~~~~~~
Databases management and definition
:license: MIT
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DataManager:

    __db_engine = create_engine
    __db_session = sessionmaker

    def __init__(self, user,password,host,db_name):
        Session = sessionmaker()
        self.__db_engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                user,
                password,
                host,
                db_name
            )
        )
        self.__db_session = Session(bind=self.__db_engine)