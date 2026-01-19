# calendar_app/views.py

from datetime import timedelta, datetime, date
from django.shortcuts import render
from django.utils import timezone
from home.models import Car, Booking
from django.contrib.auth.decorators import login_required
import calendar
@login_required(login_url='login_landing')
def weekly_calender(request):
        view_type = request.GET.get('view', 'week')  # week | month
        date_str = request.GET.get('date')
        if date_str:
            focus_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            focus_date = timezone.now().date()

        # 2. Calculate Week Range (Mon - Sun)
        start_of_week = focus_date - timedelta(days=focus_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        week_dates = [start_of_week + timedelta(days=i) for i in range(7)]
        # 3. Get Active Cars
        cars = Car.objects.filter(is_active=True)
        
        resource_schedule = []

        for car in cars:
            # Fetch overlap bookings: Starts before week ends AND Ends after week starts
            car_week_bookings = Booking.objects.filter(
                car=car,
                status='CONFIRMED',
                start_time__date__lte=end_of_week, 
                end_time__date__gte=start_of_week
            ).order_by('start_time')

            car_week_data = []
            for day in week_dates:
                # Check if this specific day falls within any booking's range
                active_bookings = []
                for b in car_week_bookings:
                    # Logic: Is 'day' inside the [Start, End] range?
                    if b.start_time.date() <= day <= b.end_time.date():
                        active_bookings.append(b)

                car_week_data.append({
                    'date': day,
                    'is_today': day == timezone.now().date(),
                    'bookings': active_bookings
                })
                
            resource_schedule.append({
                'car': car,
                'days': car_week_data
            })
             # MONTH VIEW (NEW)
    # =========================
            year = focus_date.year
            month = focus_date.month

            cal = calendar.Calendar(firstweekday=0)
            month_days = cal.monthdatescalendar(year, month)

            month_start = date(year, month, 1)
            month_end = date(year, month, calendar.monthrange(year, month)[1])

            month_bookings = Booking.objects.filter(
                status='CONFIRMED',
                start_time__date__lte=month_end,
                end_time__date__gte=month_start
            )

            booking_map = {}
            for booking in month_bookings:
                current = max(booking.start_time.date(), month_start)
                end = min(booking.end_time.date(), month_end)
                while current <= end:
                    booking_map.setdefault(current, []).append(booking)
                    current += timedelta(days=1)


        context = {
            'week_dates': week_dates,
            'resource_schedule': resource_schedule,
            'current_month': start_of_week.strftime('%B %Y'),
            'current_date_iso': focus_date.strftime('%Y-%m-%d'),
            'prev_week': (start_of_week - timedelta(days=7)).strftime('%Y-%m-%d'),
            'next_week': (start_of_week + timedelta(days=7)).strftime('%Y-%m-%d'),
            'today_date': timezone.now().date(),
            'view_type': view_type,
            'booking_map': booking_map,
            'month_days': month_days,
        }

        return render(request, 'calender/calender.html', context)