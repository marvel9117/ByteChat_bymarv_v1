#!/usr/python3
"""
Module file_storage serializes and
deserializes JSON types
"""

import json
import os

class FileStorage:
    """
    Serializes instances to JSON file and deserializes to JSON file.
    """
    __file_path = "file.json"
    __objects = {}


    def all(self):
        """
        Returns the dictionary __objects
        """
        return self.__objects


    def new(self, obj):
        """
         sets in __objects the obj with key <obj class name>.id
        """
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        '''
            Serializes __objects attribute to JSON file.
        '''
        obj_dict = {}

