#!/usr/bin/python
# -*- encoding: utf-8 -*-
import unittest
from dbclasses import Quadrupole, Crystal, Group
from dbclasses import create_component
from dbclasses import convert_component_to_dict, convert_all_to_dict
from dbclasses import UnknownName, UnknownType
from dbclasses import active_components

class TestCreate(unittest.TestCase):
    def test1_create_obj(self):
        '''
        Test adding ojects
        '''
        q = Quadrupole(name="Q1",
                        prop_q1=1.1,
                        prop_q2=2.2)
        c = Crystal(name='C1',
                    prop_c1=0.1,
                    prop_c2=0.2)

    def test1_create_group(self):
        '''
        Test create group
        '''
        q1 = Quadrupole(name='Q2',
                        prop_q1=1.2,
                        prop_q2=2.3)
        q2 = Quadrupole(name='Q3',
                        prop_q1=1.5,
                        prop_q2=2.6)
        c = Crystal(name='C2',
                    prop_c1=0.3,prop_c2=0.4)
        g = Group(name='G1')
        g.add_component( (q1,q2) )
        g.add_component( c )
        self.assertEqual(len(g.components),3)

    def test1_create(self):
        '''
        Testing creation of components via helper function
        Creating a tree of components:
        G3 --+-- C3
             +-- G2 --+-- Q4
                      +-- Q5
        '''
        q1 = create_component(type='Quadrupole',
                name='Q4',prop_q1=2.3)
        q2 = create_component(type='Quadrupole',
                name='Q5', prop_q1=33.)
        g1 = create_component(type='Group', name='G2')
        g1.add_component((q1,q2))
        self.assertEqual(len(g1.components),2)
        c1 = create_component(type='Crystal',
                name='C3', prop_c1=0.3)
        g2 = create_component(type='Group', name='G3')
        g2.add_component((c1,g1))
        self.assertRaises(UnknownName,
                          create_component,type='Group')
        self.assertRaises(UnknownType,
                          create_component,
                          type='Wrong',name='A')

    def test1_convert_to_dict(self):
        '''
        Testing converting components to dictionary
        '''
        # First create again the same tree structure
        q1 = create_component(type='Quadrupole',
                name='Q4',prop_q1=2.3)
        q2 = create_component(type='Quadrupole',
                name='Q5', prop_q1=33.)
        g1 = create_component(type='Group', name='G2')
        g1.add_component((q1,q2))
        c1 = create_component(type='Crystal',
                name='C3', prop_c1=0.3)
        g2 = create_component(type='Group', name='G3')
        g2.add_component((c1,g1))
        output = convert_component_to_dict(g2)
        self.assertTrue(isinstance(output,dict))
        self.assertGreater(len(active_components),0)
        converted = convert_all_to_dict(active_components)
        self.assertGreater(len(converted),0)
        self.assertTrue(isinstance(converted,list)                )

if __name__ == '__main__':
    unittest.main()