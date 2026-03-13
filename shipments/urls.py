from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    # Auth endpoints
    path('auth/register/', auth_views.RegisterView.as_view(), name='register'),
    path('auth/login/', auth_views.LoginView.as_view(), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/refresh/', auth_views.RefreshTokenView.as_view(), name='token-refresh'),

    # Customer endpoints
    path('customers/', views.CustomerListCreateView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),

    # Container endpoints
    path('containers/', views.ContainerListCreateView.as_view(), name='container-list'),
    path('containers/<int:pk>/', views.ContainerDetailView.as_view(), name='container-detail'),

    # Shipment endpoints
    path('shipments/', views.ShipmentListCreateView.as_view(), name='shipment-list'),
    path('shipments/search/', views.ShipmentSearchView.as_view(), name='shipment-search'),
    path('shipments/<int:pk>/', views.ShipmentDetailView.as_view(), name='shipment-detail'),
    path('shipments/<int:pk>/status/', views.ShipmentStatusUpdateView.as_view(), name='shipment-status'),
]
