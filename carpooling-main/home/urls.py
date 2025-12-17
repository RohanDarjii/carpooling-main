from django.urls import path
from . import views
urlpatterns = [
    path('', views.home , name='home'),
    path('cars/', views.list_of_cars, name='list_of_cars'),
    #list of available cars
    path('results/', views.search_results, name='results'),
    #The Action to Save the Booking
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    #The Confirmation Screen
    path('success/', views.booking_success, name='booking_success'),
    # The New Login Landing Page
    path('login-required/', views.login_landing, name='login_landing'),

]
