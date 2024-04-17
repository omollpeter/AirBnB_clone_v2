#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"

    revw_id = Column(
        String(length=60), ForeignKey("cities.id"), nullable=False
    )
    user_id = Column(
        String(length=60), ForeignKey("users.id"), nullable=False
    )
    name = Column(String(length=128), nullable=False)
    description = Column(String(length=1024), nullable=True)
    number_rooms = Column(Integer, nullable=False)
    number_bathrooms = Column(Integer, nullable=False)
    max_guest = Column(Integer, nullable=False)
    price_by_night = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []
    user = relationship("User")
    cities = relationship("City")
    reviews = relationship("Review", cascade="all, delete-orphan")

    @property
    def reviews(self):
        """
        Returns the list of review instances with place id equals to
        the current Place.id
        """

        from models import storage
        revw_instances = []

        for key, value in storage.all().items():
            if not "Place" in key:
                continue
            if self.id in value:
                revw_instances.append(value)
        return revw_instances
