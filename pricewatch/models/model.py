from abc import ABCMeta, abstractmethod
from typing import Dict, List, TypeVar, Type, Union
from pricewatch.common import database

T = TypeVar('T', bound='Model')


class Model(metaclass=ABCMeta):

    collection: str
    _id: str

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    def save_to_db(self):
        database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_db(self):
        database.remove(self.collection, {"_id": self._id})

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        return [cls(**elem) for elem in database.find(cls.collection, {})]

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        return cls.find_one_by("_id", _id)

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T:
        return cls(**database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> List[T]:
        return [cls(**elem) for elem in database.find(cls.collection, {attribute: value})]
