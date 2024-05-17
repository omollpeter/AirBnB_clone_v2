#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import os


HBNB_TYPE_STORAGE = os.environ.get("HBNB_TYPE_STORAGE")


place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column(
        'place_id',
        String(length=60),
        ForeignKey("places.id"),
        primary_key=True, nullable=False
    ),
    Column(
        'amenity_id',
        String(length=60),
        ForeignKey("amenities.id"),
        primary_key=True, nullable=False
    )
)


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"

    city_id = Column(
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
    if HBNB_TYPE_STORAGE == "db":
        reviews = relationship("Review", cascade="all, delete-orphan")
        amenities = relationship(
            "Amenity", secondary=place_amenity, viewonly=False
        )

    if HBNB_TYPE_STORAGE == "file":
        @property
        def reviews(self):
            """
            Returns the list of review instances with place id equals to
            the current Place.id
            """

            from models import storage
            revw_instances = []

            for key, value in storage.all().items():
                if "Review" not in key:
                    continue
                if self.id in value:
                    revw_instances.append(value)
            return revw_instances

        @property
        def amenities(self):
            """
            Returns the list of amenity instances based on amenity_ids
            """
            from models import storage
            amenity_instances = []

            for key, value in storage.all().items():
                if "Amenity" not in key:
                    continue
                if self.id in value and key.split('.')[1] in self.amenity_ids:
                    amenity_instances.append(value)
            return amenity_instances

        @amenities.setter
        def amenities(self, amenity):
            if amenity:
                self.amenity_ids.append(amenity.id)
