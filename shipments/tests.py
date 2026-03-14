from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Customer, Container, Shipment
from datetime import date

class BaseTestCase(TestCase):
    def setUp(self):
        # Create test user and authenticate
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        # Create test data
        self.customer = Customer.objects.create(
            name='Test Customer',
            email='test@example.com',
            phone='4161234567'
        )
        self.container = Container.objects.create(
            container_number='TEST-001',
            condition='good'
        )
        self.shipment = Shipment.objects.create(
            tracking_number='TEST-SHIP-001',
            customer=self.customer,
            container=self.container,
            origin='Toronto',
            destination='Vancouver',
            status='created',
            weight_kg=1000.00,
            estimated_delivery=date(2025, 4, 1)
        )




class CustomerAPITest(BaseTestCase):
    def test_get_customers_returns_200(self):
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_customer_returns_201(self):
        data = {
            'name': 'New Customer',
            'email': 'new@example.com',
            'phone': '4169999999'
        }
        response = self.client.post('/api/customers/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Customer')

    def test_create_customer_missing_email_returns_400(self):
        data = {'name': 'No Email Customer'}
        response = self.client.post('/api/customers/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_customer_with_shipments_returns_409(self):
        response = self.client.delete(f'/api/customers/{self.customer.id}/')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class ShipmentAPITest(BaseTestCase):
    def test_get_shipments_returns_200(self):
        response = self.client.get('/api/shipments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_shipment_returns_201(self):
        data = {
            'tracking_number': 'TEST-SHIP-002',
            'customer': self.customer.id,
            'container': self.container.id,
            'origin': 'Montreal',
            'destination': 'Calgary',
            'status': 'created',
            'weight_kg': 500.00,
            'estimated_delivery': '2025-04-15'
        }
        response = self.client.post('/api/shipments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_shipment_status(self):
        response = self.client.patch(
            f'/api/shipments/{self.shipment.id}/status/',
            {'status': 'in_transit'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'in_transit')

    def test_invalid_status_returns_400(self):
        response = self.client.patch(
            f'/api/shipments/{self.shipment.id}/status/',
            {'status': 'flying'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_request_returns_401(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get('/api/shipments/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ContainerAPITest(BaseTestCase):
    def test_get_containers_returns_200(self):
        response = self.client.get('/api/containers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_container_returns_201(self):
        data = {
            'container_number': 'TEST-002',
            'condition': 'good'
        }
        response = self.client.post('/api/containers/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_container_with_shipments_returns_409(self):
        response = self.client.delete(f'/api/containers/{self.container.id}/')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class AuthAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_returns_201(self):
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'newuser@example.com'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_returns_200(self):
        User.objects.create_user(username='loginuser', password='loginpass123')
        data = {'username': 'loginuser', 'password': 'loginpass123'}
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_wrong_password_returns_401(self):
        User.objects.create_user(username='loginuser2', password='correctpass')
        data = {'username': 'loginuser2', 'password': 'wrongpass'}
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)