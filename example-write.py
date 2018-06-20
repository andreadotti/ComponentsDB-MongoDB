#!/usr/bin/python
# -*- encoding: utf-8 -*-

import dbclasses

# Create components passing a dictionary of properties
# type and name are mandatory

q1 = dbclasses.create_component(
    type='Quadrupole' ,
    name='Q1',
    prop_q1=1.2,
    prop_q2=1.3
    )

c1 = dbclasses.create_component(
    type='Crystal',
    name='C1',
    prop_c1=0.1,
    prop_c2=0.2
    )

# Can be created also using directly classes
q2 = dbclasses.Quadrupole(name='Q2', prop_qq=3.2)

# User defined components can be created
# inheriting from base class.
# An example of a component that has a single
# property. name is mandatory
# derived class should set the type
class MyComponentType(dbclasses.Component):
    def __init__(self,name,prop,**kwargs):
        kwargs.update({'name':name, 'type':self.__class__.__name__,'prop':prop})
        dbclasses.Component.__init__(self,
            **kwargs
            )

custom = MyComponentType(name="M1",prop=[1,2,3])

# We now create a group of components 
g = dbclasses.Group("G1")
g.add_component( [q1,q2,c1,custom] )

# There is a list of all components created
print('Now I have created %d componets'%len(dbclasses.active_components))
print('There are %d known component types: '%len(dbclasses.__component_type_registry__),end='')
print(dbclasses.__component_type_registry__.keys())

# Convert all components to a data-structure that can be
output = dbclasses.convert_all_to_dict( dbclasses.active_components )
print('The current active components, transformed to a dictionary are:')
print('==========================')
print(output)
print('==========================')

# Can be saved to json directly
import json
with open('components_dump.json','w') as f:
    json.dump(output,f)

db = dbclasses.DataBase
db.connect()
db.write_collection(dbclasses.active_components)
from pymongo import MongoClient
client = MongoClient()
db = client.components
collection = db.example

collection.insert_many(output)

client.close()