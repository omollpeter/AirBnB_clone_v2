#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel):
    """ State class """

    __tablename__ = "states"

    name = Column(String(length=128), nullable=False)
    cities = relationship(
        "City", cascade="all, delete",
        back_populates="state"
    )

    @property
    def cities(self):
        """
        Returns of city instances with state id equals to current
        state id
        """
        from models import storage
        city_instances = []

        for value in storage.all(City).values():
            if self.id in value:
                city_instances.append(value)
        return city_instances


City.state = relationship("State", back_populates="cities")
