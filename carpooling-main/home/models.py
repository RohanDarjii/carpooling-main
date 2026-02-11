from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Car(models.Model):
    LOCATION_CHOICES = (
        ('koblenz', 'Koblenz'),
        ('frankfurt', 'Frankfurt'),
        ('berlin', 'Berlin'),
    )
    model_name = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    is_active = models.BooleanField(default=True)
    last_service_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when the car was last serviced"
    )

    SERVICE_INTERVAL_DAYS = 90  # 3 months

    def is_service_due(self):
        """
        Returns True if service is overdue
        """
        if not self.last_service_date:
            return True  # Never serviced → overdue

        due_date = self.last_service_date + timedelta(days=self.SERVICE_INTERVAL_DAYS)
        return timezone.now().date() > due_date

    def service_status(self):
        return "Overdue" if self.is_service_due() else "OK"

    service_status.short_description = "Service Status"
    remarks = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.model_name} ({self.license_plate})"

class Booking(models.Model):
    booking_id = models.CharField(
    max_length=12,
    unique=True,
    editable=False,
    db_index=True

    )
    user_email = models.EmailField(null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    destination = models.CharField(max_length=200, blank=True)
    project_no = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, default='CONFIRMED')
    booked_by = models.CharField(max_length=150, help_text="Name of the user who booked the car from Microsoft login")
    client_name = models.CharField(max_length=150, blank=True,null=True, help_text="Name of the passenger for whom the car is booked")
    client = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_bookings"
    )
    current_time = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()
        super().save(*args, **kwargs)

    def generate_booking_id(self):
        return f"BK-{uuid.uuid4().hex[:8].upper()}"

    def __str__(self):
        return self.booking_id
    
    def get_client_display(self):
        if self.client:
            return self.client.get_full_name() or self.client.email
        return self.booked_by

    def __str__(self):
        if self.client_name:
            return f"Booking for {self.car} booked by {self.booked_by} for {self.client_name} from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')} ---> {self.destination}"
        else:
            return f"Booking for {self.car} booked by {self.booked_by} from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')} ---> {self.destination}"