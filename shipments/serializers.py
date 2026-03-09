from rest_framework import serializers
from .models import Customer,Container, Shipment

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields = ['id', 'name', 'email', 'phone', 'created_at']
        read_only_fields = ['created_at']


class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Container
        fields = ['id', 'container_number', 'condition', 'created_at']
        read_only_fields = ['created_at']


class ShipmentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(
        source='customer.name',
        read_only=True
    )
    container_number = serializers.CharField(
        source='container.container_number',
        read_only=True
    )

    class Meta:
        model = Shipment
        fields = [
            'id',
            'tracking_number',
            'customer',
            'customer_name',
            'container',
            'container_number',
            'origin',
            'destination',
            'status',
            'weight_kg',
            'estimated_delivery',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']