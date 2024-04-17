#!/usr/bin/python3
"""
This module contains class definition DBStorage that manages storage in a
relational database using SQLAlchemy

"""


import os
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


HBNB_ENV = os.environ.get("HBNB_ENV")
HBNB_MYSQL_USER = os.environ.get("HBNB_MYSQL_USER")
HBNB_MYSQL_PWD = os.environ.get("HBNB_MYSQL_PWD")
HBNB_MYSQL_HOST = os.environ.get("HBNB_MYSQL_HOST")
HBNB_MYSQL_DB = os.environ.get("HBNB_MYSQL_DB")


class DBStorage:
    """Defines a database storage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """Initializes instance attributes"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}:3306/{}'.format(
                HBNB_MYSQL_USER,
                HBNB_MYSQL_PWD,
                HBNB_MYSQL_HOST,
                HBNB_MYSQL_DB
            ),
            pool_pre_ping=True
        )


        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """
        Query on the current db session depending on the class name
        or None

        Returns:
            return (dict): Dictionary containing objects 
        """
        

        objs = {}
        if cls is None:
            results = self.__session.query(
                State, City, User, Place, Review
            ).all()

            for result in results:
                key = result.__class__.__name__ + "." + result.id
                objs[key] = result
        else:
            results = self.__session.query(cls).all()

            for result in results:
                key = result.__class__.__name__ + "." + result.id
                objs[key] = result

        return objs

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all the changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database then creates a db session
        """
        Base.metadata.create_all(self.__engine)

        Session = scoped_session(sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        )
        self.__session = Session()
