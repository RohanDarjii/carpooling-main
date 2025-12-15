from django.shortcuts import get_object_or_404, render,redirect
from datetime import datetime
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_time
from django.contrib import messages
from . import models
# Create your views here.
def home(request):
    context = {
        'form': request.GET,
    }
    return render(request, 'home/home.html', context)

def list_of_cars(request):
    cars = models.Car.objects.all()
    return render(request, 'home/list_of_cars.html', {'cars': cars})

#will create a funtion for converting string to datetime object
def get_datetimes(date_str, time_str):
    dt = datetime.combine(parse_date(date_str), parse_time(time_str))
    return timezone.make_aware(dt, timezone.get_current_timezone())

def search_results(request):
    context = {'available_cars': [],
               'errors': [],
               }
    f_date = request.GET.get('from_date')
    t_date = request.GET.get('to_date')
    f_time = request.GET.get('time_from')
    t_time = request.GET.get('time_to')
    dest = request.GET.get('destination')
    project_no = request.GET.get('project_no')

    # Store params to pass them to the template (and later to the booking view)
    context['search_params'] = {
        'from_date': f_date, 'to_date': t_date,
        'time_from': f_time, 'time_to': t_time,
        'destination': dest, 'project_no': project_no
    }
    if not all([f_date, t_date, f_time, t_time, project_no]):
        context['errors'].append("Please fill in all required fields.")
    try:
        start_full = get_datetimes(f_date, f_time)
        end_full = get_datetimes(t_date, t_time)
        #Prevent Past Dates Booking
        current_time = timezone.now()
        if start_full < current_time:
            context['errors'].append("You cannot book a ride in the past.")
            return render(request, 'home/results.html', context)
        # --- NEW LOGIC END ---
        if start_full >= end_full:
            context['errors'].append("End date/time must be after start date/time.")
        else:
            #Find Busy Cars
            busy_ids = models.Booking.objects.filter(
                status='CONFIRMED',
                start_time__lt=end_full,
                end_time__gt=start_full
            ).values_list('car_id', flat=True)
            #Find Available Cars
            context['available_cars'] = models.Car.objects.filter(
                is_active=True
            ).exclude(id__in=busy_ids)
    except Exception as e:
        context['errors'].append("Invalid date/time format.")
    return render(request, 'home/results.html', context)
    
def book_car(request, car_id):
    if request.method == 'POST':
        f_date = request.POST.get('from_date')
        t_date = request.POST.get('to_date')
        f_time = request.POST.get('time_from')
        t_time = request.POST.get('time_to')
        dest = request.POST.get('destination')
        project_no = request.POST.get('project_no')
        try:
            start_full = get_datetimes(f_date, f_time)
            end_full = get_datetimes(t_date, t_time)
            car = get_object_or_404(models.Car, id=car_id)
            #just checking the race condition if two users are booking the same car at the same time
            is_booked = models.Booking.objects.filter(
                car=car,
                status='CONFIRMED',
                start_time__lt=end_full,
                end_time__gt=start_full
            ).exists()
            if is_booked:
                messages.error(request, "Sorry, this car {car.model_name} has just been booked for the selected time slot.")
                return redirect('home')
            
            #if not booked, create the booking
            models.Booking.objects.create(
                car=car,
                start_time=start_full,
                end_time=end_full,
                destination=dest,
                project_no=project_no,
                status='CONFIRMED',
            )
            return redirect('booking_success')
        
        except Exception :
            messages.error(request, "An error occurred while processing your booking. Please try again.")
            return redirect('home')
        
    return redirect('home')

def booking_success(request):
    return render(request, 'home/success.html')


        

        


