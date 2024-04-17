#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.state import State

class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    

    __tablename__ = "cities"

    state_id = Column(
        String(length=60),
        ForeignKey("states.id"),
        nullable=False
    )
    name = Column(String(length=128), nullable=False)
    state = relationship("State", backref="cities")
