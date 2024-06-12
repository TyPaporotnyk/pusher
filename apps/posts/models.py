from django.db import models
from django.utils.text import slugify

from apps.base.models import TimedBaseModel
from apps.posts.utils.upload import get_post_image_path


class Post(TimedBaseModel):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=500)
    description = models.TextField()
    slug = models.SlugField(max_length=500)
    url = models.URLField(max_length=500)
    group_name = models.CharField(max_length=500, blank=True, null=True)
    group_url = models.URLField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class PostImage(TimedBaseModel):
    image = models.ImageField(upload_to=get_post_image_path, blank=True, null=True)
    original_image_url = models.URLField(max_length=500, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        if self.image:
            return self.image.url
        else:
            return self.original_image_url
