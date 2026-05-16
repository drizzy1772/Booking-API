from celery import shared_task
from .models import Booking

@shared_task
def send_booking_email(booking_id):
    booking = Booking.objects.get(id=booking_id)
    print(f"Sending email to user {booking.user.email} for booking {booking_id}")

@shared_task
def generate_ticket_pdf(booking_id):
    booking = Booking.objects.get(id=booking_id)
    print(f"Generating PDF ticket for booking {booking_id}")
