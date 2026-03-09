from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Customer, Container, Shipment
from .serializers import (
    CustomerSerializer,
    ContainerSerializer,
    ShipmentSerializer
)


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ContainerListCreateView(generics.ListCreateAPIView):
    queryset = Container.objects.all().order_by('-created_at')
    serializer_class = ContainerSerializer


class ContainerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer


class ShipmentListCreateView(generics.ListCreateAPIView):
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        return Shipment.objects.select_related(
            'customer', 'container'
        ).all().order_by('-created_at')


class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        return Shipment.objects.select_related(
            'customer', 'container'
        ).all()


class ShipmentStatusUpdateView(APIView):
    def patch(self, request, pk):
        shipment = get_object_or_404(Shipment, pk=pk)
        new_status = request.data.get('status')

        valid_statuses = ['created', 'in_transit', 'arrived', 'delivered', 'cancelled']
        if new_status not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Must be one of: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        shipment.status = new_status
        shipment.save()
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)