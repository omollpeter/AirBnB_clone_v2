#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"

    name = Column(String(length=128), nullable=False)
    cities = relationship(
        "City", cascade="all, delete-orphan",
        backref="state"
    )

    @property
    def cities(self):
        """
        Returns of city instances with state id equals to current
        state id
        """
        from models import storage
        city_instances = []

        for key, value in storage.all().items():
            if not "City" in key:
                continue
            if self.id in value:
                city_instances.append(value)
        return city_instances
