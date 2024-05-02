#!/usr/bin/python3
""" DBStorage Module for HBNB project """
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


db_classes = {
    'User': User,
    'Place': Place,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Review': Review
}


class DBStorage:
    """ Database storage class """

    __engine = None
    __session = None

    def __init__(self):
        """ Initialize DBStorage """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session """
        objs = {}
        if cls:
            query = self.__session.query(db_classes[cls])
            for obj in query:
                objs["{}.{}".format(cls, obj.id)] = obj
        else:
            for cls in db_classes.values():
                query = self.__session.query(cls)
                for obj in query:
                    objs["{}.{}".format(cls.__name__, obj.id)] = obj
        return objs

    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the db and create the current db session """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))
