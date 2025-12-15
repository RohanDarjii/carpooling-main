from django.urls import path
from . import views

urlpatterns = [
    path('', views.weekly_calender, name='calender_view'),
]