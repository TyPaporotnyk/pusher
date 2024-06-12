import factory
from factory.django import DjangoModelFactory

from apps.posts.models import Post


class PostModelFactory(DjangoModelFactory):
    description = factory.Faker("text")
    url = factory.Faker("url")

    class Meta:
        model = Post
