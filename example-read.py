#!/usr/bin/python
# -*- encoding: utf-8 -*-

from dbclasses import Component, Quadrupole, Group, Crystal
from dbclasses import create_component, resolve_reference
from dbclasses import DataBase

# This is just to have the same component as
# in the writer example, in real life this
# would be in a user-defined module
class MyComponentType(Component):
    def __init__(self,name,prop,**kwargs):
        kwargs.update({
            'name':name,
            'prop':prop,
            'type':self.__class__.__name__
            })
        Component.__init__(self,**kwargs)

# from pymongo import MongoClient

db = DataBase()
db.connect()
components = db.read_all() #or read by name

import pprint
print('List of components:')
pprint.pprint(components)
print('Last component is a group, here are the data:')
pprint.pprint(components[-1].__dict__)