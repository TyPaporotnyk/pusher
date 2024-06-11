import factory
from django.template.defaultfilters import slugify
from factory.django import DjangoModelFactory

from apps.posts.models import Post


class PostModelFactory(DjangoModelFactory):
    title = factory.Faker("first_name")
    description = factory.Faker("text")
    slug = slugify(title)
    url = factory.Faker("url")

    class Meta:
        model = Post
