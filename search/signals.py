from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry


@receiver(post_save)
def update_document(**kwargs):
    instances = kwargs['instance']
    registry.update(instances)
