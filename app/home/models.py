# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from sqlalchemy import Binary, Column, Integer, String, Date, Numeric, update, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app import db

class Clients(db.Model):

    __tablename__ = 'Clients'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    telephone = Column(String)
    client_type = Column(String)
    pro_bono = Column(String)
    sessions = relationship('Sessions', back_populates='clients')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
                
            setattr(self, property, value)
    
    def update(self, **kwargs):
        # just pass all the values back into the __init__ function to update the values
        # instead of duplicating the code
        self.__init__(**kwargs)
    
    def values(self):
        return({
            'id'          : self.id,
            'user_id'     : self.user_id,
            'first_name'  : self.first_name,
            'last_name'   : self.last_name,
            'email'       : self.email,
            'telephone'   : self.telephone,
            'client_type' : self.client_type,
            'pro_bono'    : self.pro_bono
        })

    def table_columns():
        return([
            { 'field': 'id',          'title': 'ID',          'visible': False },
            { 'field': 'user_id',     'title': 'user_id',     'visible': False },
            { 'field': 'first_name',  'title': 'First Name',  'sortable': True },
            { 'field': 'last_name',   'title': 'Last Name',   'sortable': True },
            { 'field': 'email',       'title': 'Email',       'sortable': True },
            { 'field': 'telephone',   'title': 'Telephone',   'sortable': True },
            { 'field': 'client_type', 'title': 'Client Type', 'sortable': True },
            { 'field': 'pro_bono',    'title': 'Pro Bono',    'sortable': True },
            { 'field': 'actions',     'title': 'Actions', 'align': 'center', 'clickToSelect': False, 'events': 'window.actionEvents', 'formatter': 'actionFormatter' }
        ])

    def __repr__(self):
        return str(self.values())

class Sessions(db.Model):

    __tablename__ = 'Sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    date = Column(Date)
    duration = Column(Numeric)
    client_id = Column(Integer, ForeignKey('Clients.id'))
    clients = relationship('Clients', back_populates='sessions')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
                
            setattr(self, property, value)
    
    def update(self, **kwargs):
        # just pass all the values back into the __init__ function to update the values
        # instead of duplicating the code
        self.__init__(**kwargs)
    
    def values(self):
        return({
            'id'          : self.id,
            'user_id'     : self.user_id,
            'client_id'   : self.client_id,
            'date'        : self.date,
            'duration'    : self.duration
        })

    #Define columns shown on Bootstrap-Tables when this data is queries
    def table_columns():
        return([
            { 'field': 'id',          'title': 'ID',          'visible': False },
            { 'field': 'user_id',     'title': 'user_id',     'visible': False },
            { 'field': 'first_name',  'title': 'First Name',  'sortable': True },
            { 'field': 'last_name',   'title': 'Last Name',   'sortable': True },
            { 'field': 'email',       'title': 'Email',       'sortable': True },
            { 'field': 'telephone',   'title': 'Telephone',   'sortable': True },
            { 'field': 'client_type', 'title': 'Client Type', 'sortable': True },
            { 'field': 'pro_bono',    'title': 'Pro Bono',    'sortable': True },
            { 'field': 'date',        'title': 'Date',        'sortable': True },
            { 'field': 'duration',    'title': 'Duration',    'sortable': True },
            { 'field': 'actions',     'title': 'Actions', 'align': 'center', 'clickToSelect': False, 'events': 'window.actionEvents', 'formatter': 'actionFormatter' }
        ])

    def __repr__(self):
        return str(self.values())