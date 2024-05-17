#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import os


HBNB_TYPE_STORAGE = os.environ.get("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"

    name = Column(String(128), nullable=False)

    if HBNB_TYPE_STORAGE == "db":
        cities = relationship(
            "City", cascade="all, delete-orphan"
        )

    else:
        @property
        def cities(self):
            """
            Returns of city instances with state id equals to current
            state id
            """
            from models import storage
            from models.city import City
            city_instances = []

            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_instances.append(city)
            return city_instances
