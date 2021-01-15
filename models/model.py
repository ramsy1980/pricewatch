from abc import ABCMeta, abstractmethod
from typing import List
from uuid import uuid4
from common.database import database

class Model(metaclass=ABCMeta):
    collection: str = None

    def __init__(self, *args, **kwargs):
        _id = kwargs
        self._id = _id | uuid4().hex

    @abstractmethod
    def json(self):
        raise NotImplementedError

    def save_to_db(self):
        database.insert(self.collection, self.json())

    def remove_from_db(self):
        database.remove(self.collection, {"_id: {self._id}"})

    @classmethod
    def all(cls) -> List:
        return [cls(**elem) for elem in database.find(cls.collection, {})]

    @classmethod
    def get_by_id(cls, _id):
        return cls.find_one_by("_id", _id)

    @classmethod
    def find_one_by(cls, attribute, value):
        return cls(**database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls, attribute, value):
        return [cls(**elem) for elem in database.find(cls.collection, {attribute: value})]