#!/usr/bin/python3
"""
Module file_storage serializes and
deserializes JSON types
"""
import json
import os
from models.base_model import BaseModel

class FileStorage:
    """
    Serializes instances to JSON file and deserializes to JSON file.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        Arguments:
                obj : An instance object.
        """
        if obj:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        '''
        Serializes __objects attribute to JSON file.
        '''
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = {}

        obj_dict = existing_data.copy()

        for key, obj in self.__objects.items():
            obj_dict[key] = obj.to_dict()

        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        """
        classes = {'BaseModel': BaseModel}

        try:
            with open(self.__file_path, mode="r", encoding="utf-8") as f:
                reloaded = json.load(f)
                for key, val in reloaded.items():
                    class_name = val.get("__class__")
                    if class_name in classes:
                        class_ = classes[class_name]  # Retrieve the class object from dictionary
                        val.pop("__class__")  # Remove the "__class__" key from the dictionary
                        self.__objects[key] = class_(**val)  # Instantiate the class object
                    else:
                        print(f"Unknown class type '{class_name}', skipping...")
        except Exception as e:
            print(f"Error reloading objects: {e}")

