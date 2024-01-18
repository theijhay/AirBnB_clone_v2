#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import models


class City(BaseModel):
    """ The city class, contains state ID and name """
    state_id = ""
    name = ""
    
"""Representation of city """
__tablename__ = 'cities'

state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
name = Column(String(128), nullable=False)
places = relationship("Place", backref="cities")