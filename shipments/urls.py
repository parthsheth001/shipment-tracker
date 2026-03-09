from django.urls import path
from . import views

urlpatterns = [
    # Customer endpoints
    path('customers/', views.CustomerListCreateView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),

    # Container endpoints
    path('containers/', views.ContainerListCreateView.as_view(), name='container-list'),
    path('containers/<int:pk>/', views.ContainerDetailView.as_view(), name='container-detail'),

    # Shipment endpoints
    path('shipments/', views.ShipmentListCreateView.as_view(), name='shipment-list'),
    path('shipments/<int:pk>/', views.ShipmentDetailView.as_view(), name='shipment-detail'),
    path('shipments/<int:pk>/status/', views.ShipmentStatusUpdateView.as_view(), name='shipment-status'),
]