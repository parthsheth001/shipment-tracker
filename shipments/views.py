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
from django.db.models import ProtectedError
from django.core.cache import cache
from django.conf import settings
from .tasks import send_shipment_notification
from .documents import ShipmentDocument


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'error': 'Cannot delete this customer because they have shipments attached. Remove the shipments first.'},
                status=status.HTTP_409_CONFLICT
            )


class ContainerListCreateView(generics.ListCreateAPIView):
    queryset = Container.objects.all().order_by('-created_at')
    serializer_class = ContainerSerializer


class ContainerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Container.objects.all()
    serializer_class = ContainerSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {'error': 'Cannot delete this container because it has shipments attached. Remove the shipments first.'},
                status=status.HTTP_409_CONFLICT
            )


class ShipmentListCreateView(generics.ListCreateAPIView):
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        return Shipment.objects.select_related(
            'customer', 'container'
        ).all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        cache_key = 'shipment_list'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response({
                'source': 'cache',
                'data': cached_data
            })

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        cache.set(cache_key, serializer.data, settings.CACHE_TTL)

        return Response({
            'source': 'database',
            'data': serializer.data
        })

    def perform_create(self, serializer):
        shipment = serializer.save()
        cache.delete('shipment_list')
        # Fire async notification — doesn't make client wait
        send_shipment_notification.delay(shipment.id, 'created')


class ShipmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShipmentSerializer

    def get_queryset(self):
        return Shipment.objects.select_related(
            'customer', 'container'
        ).all()

    def perform_update(self, serializer):
        serializer.save()
        cache.delete('shipment_list')

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete('shipment_list')


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
        cache.delete('shipment_list')
        # Fire async notification
        send_shipment_notification.delay(shipment.id, new_status)
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)


class ShipmentSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        status_filter = request.query_params.get('status', '').strip()
        min_weight = request.query_params.get('min_weight', None)
        max_weight = request.query_params.get('max_weight', None)

        if not query and not status_filter and not min_weight and not max_weight:
            return Response(
                {'error': 'Provide at least one search parameter: q, status, min_weight, max_weight'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Start with a search object
        search = ShipmentDocument.search()

        # Full text search across multiple fields
        if query:
            search = search.query(
                'multi_match',
                query=query,
                fields=[
                    'tracking_number',
                    'origin',
                    'destination',
                    'customer_name',
                    'container_number',
                ]
            )

        # Filter by status (exact match)
        if status_filter:
            search = search.filter('term', status=status_filter)

        # Filter by weight range
        if min_weight or max_weight:
            weight_range = {}
            if min_weight:
                weight_range['gte'] = float(min_weight)
            if max_weight:
                weight_range['lte'] = float(max_weight)
            search = search.filter('range', weight_kg=weight_range)

        # Execute search
        response = search.execute()

        # Format results
        results = []
        for hit in response:
            results.append({
                'id': hit.meta.id,
                'tracking_number': hit.tracking_number,
                'origin': hit.origin,
                'destination': hit.destination,
                'status': hit.status,
                'customer_name': hit.customer_name,
                'container_number': hit.container_number,
                'weight_kg': hit.weight_kg,
                'score': hit.meta.score,
            })

        return Response({
            'total': response.hits.total.value,
            'results': results
        })