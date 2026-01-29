from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    change_list_template = "admin/home/car/change_list.html"
    list_display = (
        'model_name',
        'license_plate',
        'location',
        'is_active',
    )

admin.site.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    change_list_template = "admin/home/booking/change_list.html"

    list_filter = (
        'status',
        'car__location',
        'start_time',
    )

    search_fields = (
        'car__model_name',
        'car__license_plate',
        'booked_by',
        'client_name',
        'destination',
        'project_no',
    )
