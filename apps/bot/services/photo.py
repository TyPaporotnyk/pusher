from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

from apps.bot.models.photos import Photo


class BasePhotoRepository(ABC):

    @staticmethod
    @abstractmethod
    def get_photo_by_url(url: str) -> Photo:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create(url: str) -> Photo:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def update_photo_id(cls, photo_url: str, photo_id: str) -> Photo:
        raise NotImplementedError


class PhotoRepository(BasePhotoRepository):

    @staticmethod
    def create(photo_url: str) -> Photo:
        pass

    @staticmethod
    def get_photo_by_url(photo_url: str) -> Photo:
        return Photo.objects.filter(photo_url=photo_url).first()

    @classmethod
    def update_photo_id(cls, photo_url: str, photo_id: str) -> Photo:
        photo = cls.get_photo_by_url(photo_url)
        photo.photo_id = photo_id
        photo.save()

        return photo


@dataclass(frozen=True)
class PhotoService:
    photo_repository: PhotoRepository

    def get_photo_from_url(self, photo_url: str) -> Photo:
        pass


@dataclass(frozen=True)
class PhotoLoaderService:
    photo_repository: PhotoRepository

    def save_not_loaded_photos(self, grouped_photo_urls: zip):
        not_loaded_photos = self._get_not_loaded_photos_from_group(grouped_photo_urls)

        for not_loaded_photo in not_loaded_photos:
            self.photo_repository.update_photo_id(not_loaded_photo[1], not_loaded_photo[0])

    @staticmethod
    def _get_not_loaded_photos_from_group(grouped_photo_urls: zip) -> list[Union[str, str]]:
        grouped_photo_urls = [(group_element[0], group_element[1]) for group_element in grouped_photo_urls]
        return list(filter(lambda x: x[0] != [1], grouped_photo_urls))
