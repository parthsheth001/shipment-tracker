from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Shipment
from .documents import ShipmentDocument


@receiver(post_save, sender=Shipment)
def update_shipment_index(sender, instance, **kwargs):
    ShipmentDocument().update(instance)


@receiver(post_delete, sender=Shipment)
def delete_shipment_index(sender, instance, **kwargs):
    ShipmentDocument().update(instance, action='delete')