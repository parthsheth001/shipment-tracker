import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from shipments.models import Customer, Container, Shipment
from datetime import date

# Clear existing data
Shipment.objects.all().delete()
Container.objects.all().delete()
Customer.objects.all().delete()

# Create Customers
c1 = Customer.objects.create(name="Acme Logistics", email="acme@example.com", phone="4161234567")
c2 = Customer.objects.create(name="Northern Freight", email="northern@example.com", phone="4169876543")
c3 = Customer.objects.create(name="Pacific Cargo", email="pacific@example.com", phone="6041112222")
c4 = Customer.objects.create(name="Great Lakes Shipping", email="greatlakes@example.com", phone="4163334444")
c5 = Customer.objects.create(name="Maple Trade Co", email="maple@example.com", phone="4165556666")

# Create Containers
con1 = Container.objects.create(container_number="CONT-001", condition="good")
con2 = Container.objects.create(container_number="CONT-002", condition="damaged")
con3 = Container.objects.create(container_number="CONT-003", condition="under_repair")
con4 = Container.objects.create(container_number="CONT-004", condition="good")
con5 = Container.objects.create(container_number="CONT-005", condition="good")

# Create Shipments
Shipment.objects.create(tracking_number="SHIP-001", customer=c1, container=con1, origin="Toronto", destination="Vancouver", status="delivered", weight_kg=1200.50, estimated_delivery=date(2025, 3, 1))
Shipment.objects.create(tracking_number="SHIP-002", customer=c1, container=con2, origin="Montreal", destination="Calgary", status="in_transit", weight_kg=850.00, estimated_delivery=date(2025, 3, 10))
Shipment.objects.create(tracking_number="SHIP-003", customer=c2, container=con3, origin="Vancouver", destination="Toronto", status="created", weight_kg=2000.00, estimated_delivery=date(2025, 3, 15))
Shipment.objects.create(tracking_number="SHIP-004", customer=c2, container=con4, origin="Calgary", destination="Ottawa", status="arrived", weight_kg=500.75, estimated_delivery=date(2025, 2, 28))
Shipment.objects.create(tracking_number="SHIP-005", customer=c3, container=con5, origin="Toronto", destination="Halifax", status="delivered", weight_kg=3200.00, estimated_delivery=date(2025, 3, 5))
Shipment.objects.create(tracking_number="SHIP-006", customer=c3, container=con1, origin="Ottawa", destination="Vancouver", status="in_transit", weight_kg=675.25, estimated_delivery=date(2025, 3, 12))
Shipment.objects.create(tracking_number="SHIP-007", customer=c4, container=con2, origin="Halifax", destination="Toronto", status="cancelled", weight_kg=920.00, estimated_delivery=date(2025, 3, 8))
Shipment.objects.create(tracking_number="SHIP-008", customer=c4, container=con3, origin="Toronto", destination="Montreal", status="created", weight_kg=1450.00, estimated_delivery=date(2025, 3, 20))
Shipment.objects.create(tracking_number="SHIP-009", customer=c5, container=con4, origin="Vancouver", destination="Calgary", status="in_transit", weight_kg=780.50, estimated_delivery=date(2025, 3, 18))
Shipment.objects.create(tracking_number="SHIP-010", customer=c5, container=con5, origin="Calgary", destination="Toronto", status="delivered", weight_kg=2100.00, estimated_delivery=date(2025, 3, 3))

print("Seed data created successfully.")
print(f"Customers: {Customer.objects.count()}")
print(f"Containers: {Container.objects.count()}")
print(f"Shipments: {Shipment.objects.count()}")