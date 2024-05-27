#!/usr/bin/python3
"""
Class basemodel in which other classes will inherit from
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    Custom base for all the classes in the AirBnb console project

    Arttributes:
        id(str): handles unique user identity
        created_at: assigns current datetime
        updated_at: updates current datetime

    Methods:
        __str__: prints the class name, id, and creates dictionary
        representations of the input values
        save(self): updates instance arttributes with current datetime
        to_dict(self): returns the dictionary values of the instance obj

    """
    def __init__(self, *args, **kwargs):
        """
        Public instance artributes initialization
        after creation
        """
        
        date_time_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for key, value in kwargs.items():
                if key == __class__:
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(value,
                            date_time_format))
                else:
                    setattr(self, key, value)

    def __str__(self):
        """
        Public instance artributes initialization
        after creation
        returns __str__: should print: [<class name>]
        (<self.id>) <self.__dict__>
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
        updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values
        of __dict__ of the instance
        serialization/deserialization process: create a dictionary
        representation with “simple object type” of our BaseModel
        """
        inst_dict = self.__dict__.copy()
        inst_dict["__class__"] = self.__class__.__name__
        inst_dict["created_at"] = self.created_at.isoformat()
        inst_dict["updated_at"] = self.updated_at.isoformat()
        return inst_dict

if __name__ == "__main__":
    user = BaseModel()
    user.name = "marvel"
    print("-------srt----")
    print(user)
    print("-----strend----")
    print("-----update time----")
    user.save()
    print(user)
    print("---------------------------")
    print("------------------------TO DICT -----------------------------")
    user_json = user.to_dict()
    print(user_json)
