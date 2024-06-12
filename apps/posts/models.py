from django.db import models

from apps.base.models import TimedBaseModel
from apps.posts.utils.upload import get_post_image_path


class Post(TimedBaseModel):
    id = models.BigAutoField(primary_key=True)
    description = models.TextField()
    url = models.URLField(max_length=500)
    group_name = models.CharField(max_length=500, blank=True, null=True)
    group_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class PostImage(TimedBaseModel):
    image = models.ImageField(upload_to=get_post_image_path, blank=True, null=True)
    original_image_url = models.URLField(max_length=500, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        if self.image:
            return self.image.url
        else:
            return self.original_image_url
