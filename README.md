# Shipment Tracker API

A production-style REST API for managing shipments, tracking status, and estimating logistics costs.

![Django CI](https://github.com/parthsheth001/shipment-tracker/actions/workflows/test.yml/badge.svg)

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** PostgreSQL
- **Cache & Broker:** Redis, RabbitMQ
- **Search:** Elasticsearch
- **Task Queue:** Celery
- **Auth:** JWT (SimpleJWT)
- **DevOps:** Docker, GitHub Actions CI/CD

## Features

- JWT Authentication (register, login, logout, token refresh)
- Full CRUD API for Shipments, Customers, Containers
- Redis caching with automatic cache invalidation
- Async notifications via Celery + RabbitMQ
- Full-text search powered by Elasticsearch
- Rate limiting middleware
- Automated test suite with GitHub Actions CI/CD

## Quick Start
```bash
# Clone the repo
git clone https://github.com/parthsheth001/shipment-tracker.git
cd shipment-tracker

# Start services
docker-compose up -d

# Activate virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register/ | Register new user |
| POST | /api/auth/login/ | Login, get tokens |
| POST | /api/auth/logout/ | Logout, blacklist token |
| GET/POST | /api/shipments/ | List / Create shipments |
| GET/PUT/DELETE | /api/shipments/{id}/ | Retrieve / Update / Delete |
| PATCH | /api/shipments/{id}/status/ | Update shipment status |
| GET | /api/shipments/search/ | Full-text search |
| GET/POST | /api/customers/ | List / Create customers |
| GET/POST | /api/containers/ | List / Create containers |