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
    path('shipments/<int:pk>/', views.ShipmentDetailView.as_view(), name='shipment-detail'),
    path('shipments/<int:pk>/status/', views.ShipmentStatusUpdateView.as_view(), name='shipment-status'),
]


# {
#     "message": "User created successfully",
#     "username": "parth",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzczMTc2MjMwLCJpYXQiOjE3NzMxNzI2MzAsImp0aSI6IjdkODlhMmQ5NjQ2ZTQxMDc5OTE0NDc5YzlhNjU0NjBiIiwidXNlcl9pZCI6IjEifQ.yEyXAYNkjUK__XwjUqw1CVpTTIGu7sfRgpgmY0LFjR4",
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3Mzc3NzQzMCwiaWF0IjoxNzczMTcyNjMwLCJqdGkiOiJlYzk4ZDUzNzhhMWI0NmY1YjE2OTNiZDdmMTFkMjkyYiIsInVzZXJfaWQiOiIxIn0.3rlvYaz5y-SgdT_ri4BsTQbvc0CZ9rg9UVCtJwz0lic"
# }