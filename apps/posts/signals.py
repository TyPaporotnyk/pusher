import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.posts.models import PostImage


@receiver(post_delete, sender=PostImage)
def delete_post_image_file(sender, instance=None, **kwargs):
    img_file_path = instance.image.path
    if os.path.exists(img_file_path):
        os.remove(img_file_path)
