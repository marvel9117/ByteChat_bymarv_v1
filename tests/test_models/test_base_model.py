#!/usr/bin/python3
"""
    All the test for the base_model are implemented here.
"""

import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
        Testing the base class model.
    """
    def setUp(self):
        '''
            Initializing instance.
        '''
        self.my_model = BaseModel()
        self.my_model.name = "Binita Rai"

    def TearDown(self):
        '''
            Removing instance.
        '''
        del self.my_model

    def test_init(self):
        """
        Test init
        """
        self.assertIsNotNone(self.my_model.id)
        self.assertIsNotNone(self.my_model.created_at)
        self.assertIsNotNone(self.my_model.updated_at)

    def test_save(self):
        """
            Checks that after updating the instance; the dates differ in the
            updated_at attribute.
        """

        old_update = self.my_model.updated_at
        self.my_model.save()
        self.assertNotEqual(self.my_model.updated_at, old_update)
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_to_dict(self):
        """
            Test to_dict if it is a dictionary and if the key
            are value are present and correct
        """

        my_model_dict = self.my_model.to_dict()

        self.assertIsInstance(my_model_dict, dict)
        self.assertEqual(my_model_dict["__class__"], "BaseModel")
        self.assertEqual(my_model_dict["id"], self.my_model.id)
        self.assertEqual(my_model_dict["created_at"],
                         self.my_model.created_at.isoformat())
        self.assertEqual(my_model_dict["updated_at"],
                         self.my_model.updated_at.isoformat())

    def test_str(self):
        """
            Test __str___ if it's output a string and also
            check some values in the string
        """

        self.assertTrue(str(self.my_model).startswith('[BaseModel]'))
        self.assertIn(self.my_model.id, str(self.my_model))
        self.assertIn(str(self.my_model.__dict__), str(self.my_model))
