from django.db import models

# Create your models here.
class Car(models.Model):
    model_name = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    remarks = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.model_name} ({self.license_plate})"

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    destination = models.CharField(max_length=200, blank=True)
    project_no = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, default='CONFIRMED')
    booked_by = models.CharField(max_length=150, help_text="Name of the user who booked the car from Microsoft login")
    client_name = models.CharField(max_length=150, blank=True,null=True, help_text="Name of the passenger for whom the car is booked")
    current_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.client_name:
            return f"Booking for {self.car} booked by {self.booked_by} for {self.client_name} from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')} ---> {self.destination}"
        else:
            return f"Booking for {self.car} booked by {self.booked_by} from {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')} ---> {self.destination}"