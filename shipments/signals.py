from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Shipment
from .documents import ShipmentDocument
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Shipment)
def update_shipment_index(sender, instance, **kwargs):
    try:
        ShipmentDocument().update(instance)
    except Exception as e:
        logger.warning(f'Elasticsearch update skipped: {e}')


@receiver(post_delete, sender=Shipment)
def delete_shipment_index(sender, instance, **kwargs):
    try:
        ShipmentDocument().update(instance, action='delete')
    except Exception as e:
        logger.warning(f'Elasticsearch delete skipped: {e}')