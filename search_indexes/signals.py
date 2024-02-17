from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry

from startup.models import Startup

@receiver(post_save)
def update_document(sender, instance, **kwargs):
    app_label = sender._meta.app_label

    if sender is Startup:
        return

    """
        Update elasticsearch records when a related model changes.
    """
    if app_label == 'startup':
        instances = instance.articles.all()
        for _instance in instances:
            registry.update(_instance)

@receiver(post_delete)
def update_document(sender, instance, **kwargs):
    app_label = sender._meta.app_label

    if sender is Startup:
        return

    """
        Update elasticsearch records when a related model has been deleted.
    """
    if app_label == 'startup':
        # re-index
        instances = Startup.objects.all()
        for _instance in instances:
            registry.update(_instance)