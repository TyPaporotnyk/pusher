import os

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.posts.models import Post, PostImage
from apps.posts.task import link_post_to_users


@receiver(post_save, sender=Post)
def post_created_handler(sender, instance, created, **kwargs):
    if created:
        link_post_to_users.apply_async((instance.id,), countdown=5)


@receiver(post_delete, sender=PostImage)
def delete_post_image_file(sender, instance=None, **kwargs):
    img_file_path = instance.image.path
    if os.path.exists(img_file_path):
        os.remove(img_file_path)
