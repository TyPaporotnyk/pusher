from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.customers.models import Customer
from apps.customers.task import load_customer_public_entities


@receiver(post_save, sender=Customer)
def customer_post_save(sender, instance, created, **kwargs):
    if created:
        load_customer_public_entities.apply_async(args=[instance.pk], countdown=1)
