#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Review(BaseModel, Base):
    """ Review classto store review information """

    __tablename__ = "reviews"

    place_id = Column(String(length=60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(length=60), ForeignKey("users.id"), nullable=False)
    text = Column(String(length=1024), nullable=False)
    user = relationship("User")
    place = relationship("Place")
