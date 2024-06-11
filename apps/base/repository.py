from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from django.db import models
from django.db.models import QuerySet

T = TypeVar("T", bound=models.Model)


class BaseRepository(ABC, Generic[T]):
    model: Type[T]

    @classmethod
    @abstractmethod
    def get(cls, **obj_field) -> T: ...

    @classmethod
    @abstractmethod
    def get_all(cls) -> QuerySet[T]: ...

    @classmethod
    @abstractmethod
    def update(cls, obj_id: int, **update_fields) -> T: ...

    @classmethod
    @abstractmethod
    def delete(cls, obj_id: int): ...


class Repository(BaseRepository[T]):

    @classmethod
    def get(cls, **obj_field) -> T:
        return cls.model.objects.get(**obj_field)

    @classmethod
    def get_all(cls) -> QuerySet[T]:
        return cls.model.objects.all()

    @classmethod
    def update(cls, obj_id: int, **update_fields) -> T:
        obj = cls.get(pk=obj_id)

        for key, value in update_fields.items():
            setattr(obj, key, value)
        obj.save()

        return obj

    @classmethod
    def delete(cls, obj_id: int):
        obj = cls.get(pk=obj_id)
        obj.delete()
