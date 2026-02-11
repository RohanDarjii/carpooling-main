from django.urls import path
from . import views

urlpatterns = [
    path('', views.weekly_calender, name='calender_view'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path("delete-booking/<int:booking_id>/", views.delete_booking, name="delete_booking"),
]