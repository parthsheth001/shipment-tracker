from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Shipment


@registry.register_document
class ShipmentDocument(Document):
    # Index related model fields explicitly
    customer_name = fields.TextField(attr='customer.name')
    customer_email = fields.KeywordField(attr='customer.email')
    container_number = fields.KeywordField(attr='container.container_number')

    class Index:
        name = 'shipments'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Shipment
        fields = [
            'tracking_number',
            'origin',
            'destination',
            'status',
            'weight_kg',
            'created_at',
        ]
        related_models = [Shipment]

    def get_queryset(self):
        return super().get_queryset().select_related(
            'customer',
            'container'
        )