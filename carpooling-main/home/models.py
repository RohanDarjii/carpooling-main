from django.db import models

# Create your models here.
class Car(models.Model):
    model_name = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.model_name} ({self.license_plate})"

class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    destination = models.CharField(max_length=200, blank=True)
    project_no = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=50, default='CONFIRMED')
    

    def __str__(self):
        return f"Booking for {self.car} from {self.start_time} to {self.end_time}"
