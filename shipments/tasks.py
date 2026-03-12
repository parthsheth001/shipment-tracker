import logging
from celery import shared_task
from django.core.cache import cache

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_shipment_notification(self, shipment_id, event_type):
    """
    Sends a notification when a shipment status changes.
    In production this would send an actual email.
    For now we log it and simulate the work.
    """
    try:
        from .models import Shipment
        shipment = Shipment.objects.select_related('customer').get(id=shipment_id)

        # Simulate notification messages
        messages = {
            'created': f'Your shipment {shipment.tracking_number} has been created and is being processed.',
            'in_transit': f'Your shipment {shipment.tracking_number} is now in transit to {shipment.destination}.',
            'arrived': f'Your shipment {shipment.tracking_number} has arrived at the destination city.',
            'delivered': f'Your shipment {shipment.tracking_number} has been delivered successfully.',
            'cancelled': f'Your shipment {shipment.tracking_number} has been cancelled.',
        }

        message = messages.get(event_type, f'Your shipment {shipment.tracking_number} has been updated.')

        # In production: send actual email here
        # For now: log it
        logger.info(f'NOTIFICATION → {shipment.customer.email}: {message}')
        print(f'NOTIFICATION → {shipment.customer.email}: {message}')

        return {
            'status': 'sent',
            'shipment_id': shipment_id,
            'customer': shipment.customer.email,
            'message': message
        }

    except Exception as exc:
        logger.error(f'Notification failed for shipment {shipment_id}: {exc}')
        raise self.retry(exc=exc, countdown=60)


@shared_task
def generate_shipment_report():
    """
    Periodic task — generates a daily summary report.
    This would be scheduled to run every day in production.
    """
    from .models import Shipment
    from django.db.models import Count, Avg

    stats = Shipment.objects.values('status').annotate(
        count=Count('id'),
        avg_weight=Avg('weight_kg')
    )

    report = {
        'total_shipments': Shipment.objects.count(),
        'by_status': list(stats),
    }

    logger.info(f'Daily Report: {report}')
    print(f'Daily Report Generated: {report}')

    return report


@shared_task
def cleanup_cancelled_shipments():
    """
    Periodic task — flags old cancelled shipments for archiving.
    """
    from .models import Shipment
    from django.utils import timezone
    from datetime import timedelta

    cutoff_date = timezone.now() - timedelta(days=30)
    old_cancelled = Shipment.objects.filter(
        status='cancelled',
        updated_at__lt=cutoff_date
    ).count()

    print(f'Found {old_cancelled} cancelled shipments older than 30 days for archiving.')
    return {'cancelled_for_archive': old_cancelled}