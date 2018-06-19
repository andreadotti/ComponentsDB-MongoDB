#!/usr/bin/python
# -*- encoding: utf-8 -*-

from dbclasses import Component, Quadrupole, Group, Crystal
from dbclasses import create_component, resolve_reference

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

from pymongo import MongoClient

client = MongoClient()
db = client.components
collection = db.example
components = []
for el in collection.find():
    print('Found a component with ID %s and type %s'%(el['id'],el['type']))
    #print(el)
    components.append(create_component(**el))

for component in components:
    component = resolve_reference(component) 

import pprint
pprint.pprint(components)
pprint.pprint(components[-1].__dict__)