#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys, inspect
from uuid import uuid1, UUID
from copy import deepcopy


# Basic exception for this module
class UnknownType(Exception):
    pass
class UnknownName(Exception):
    pass

# This contains a list of all created components
active_components = []

# All known component types a map between name and class 
# We need this to allow users to define outside of this module
# their own components and self-register them here
# see the __init__subclass__ method in base class
__component_type_registry__ = {}

class Component(object):
    '''
    A component of the database
    '''
    def __init_subclass__(cls,**kwargs):
        '''
        Register this class type in the registry
        This is done at declaration type, not at instantiation
        time. Requires python 3.6
        See
        https://stackoverflow.com/questions/5189232/how-to-auto-register-a-class-when-its-defined#5189271
        '''
        super().__init_subclass__(**kwargs)
        __component_type_registry__[cls.__name__] = cls

    def __init__(self, **kwargs):
        '''
        Create a component from the dictionary of
        values. Note should use the corresponding derived class
        '''
        if 'id' in kwargs:
            self.id = UUID('{%s}'%kwargs['id']) 
        else:
            self.id = uuid1()
        self.name = 'anonymous'
        self.type = self.__class__.__name__ 
        for k, v in kwargs.items():
            setattr(self, k, v)
        active_components.append(self)
    
    def __exit__(self, exc_type, exc_value, traceback):
        '''
        Remove instance from active components
        '''
        for i,el in enumerate(active_components):
            if el == self:
                active_components.pop(i)
                break

    def add_component(self, component):
        '''
        Add a sub-component
        '''
        if 'components' not in self.__dict__:
            self.components = []
        if isinstance(component,(list,tuple)):
            self.components.extend(component)
        else:
            self.components.append(component)

class Quadrupole(Component):
    '''
    Quadrupole component 
    '''
    def __init__(self, name , **kargs):
        kargs['name'] = name
        kargs['type'] = self.__class__.__name__
        Component.__init__(self, **kargs)

class Crystal(Component):
    '''
    Crystal component
    '''
    def __init__(self, name, **kargs):
        kargs['name'] = name
        kargs['type'] = self.__class__.__name__ 
        Component.__init__(self, **kargs)

class Group(Component):
    '''
    Generic component
    '''
    def __init__(self, name, **kwargs):
        kwargs.update({'name':name,'type':self.__class__.__name__})
        Component.__init__(self,**kwargs)

def create_component(**kwargs):
    '''
    Create a component object from arguments
    At least name and type should be provided
    '''
    if '_id' in kwargs: #Remove mongoDB ID
        del(kwargs['_id'])
    if not 'name' in kwargs:
        raise UnknownName("Specify component name") 
    if 'type' in kwargs:
        try:
            return __component_type_registry__[kwargs['type']](**kwargs)
        except KeyError as error:
            raise UnknownType("Type %s is unknown"%str(error))
    else:
        raise UnknownType("Specify type")
    raise UnknownType("'%s' is an unknown component type"%kwargs['type'])

def resolve_reference(component):
    '''
    Replace references to sub-componets expressed by ID with objects
    '''
    if 'components' in component.__dict__:
        for i, refid in enumerate(component.components):
            for el in active_components: #This should become a map
                if refid == str(el.id):
                    component.components[i]=el
    return component


def convert_component_to_dict( component ):
    '''
    Convert component to a dictionary, references to sub-components are
    converted to a list of references to id
    '''
    cc = deepcopy(component)
    outdict = cc.__dict__
    outdict['id'] = str(component.id) #Convert UUID to string for serialization
    if 'components' in outdict:
        components_list = outdict['components']
        for i, item in enumerate(components_list):
            components_list[i] = str(item.id) 
    return outdict

def convert_all_to_dict( component_list ):
    '''
    Convert all components to a list of dictionaries
    '''
    return [ convert_component_to_dict(c) for c in active_components ]

def initdb()
def write_to_collection(colletion)