import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from app_booking.forms import RoomForm
from .models import Room, Booking
from django.utils import timezone

def room_list(request):
    query = request.GET.get('name')
    date = request.GET.get('date')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    print("Query:", query)
    print("Date:", date)
    print("Start Time:", start_time)
    print("End Time:", end_time)

    if date and start_time and end_time:
        start_datetime = timezone.make_aware(timezone.datetime.strptime(date + start_time, '%Y-%m-%d%H:%M'))
        end_datetime = timezone.make_aware(timezone.datetime.strptime(date + end_time, '%Y-%m-%d%H:%M'))
        print("Start Datetime:", start_datetime)
        print("End Datetime:", end_datetime)

        rooms = Room.objects.exclude(
            bookings__start_time__gte=end_datetime,
            bookings__end_time__lte=start_datetime
        )

        if query:
            rooms = rooms.filter(name__icontains=query)
    else:
        rooms = Room.objects.all()

    print("Filtered Rooms:", rooms)

    return render(request, 'room_booking/room_list.html', {'rooms': rooms})


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    print(room_id)
    if request.method == 'POST':
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
        
        if start_time >= end_time:
            return render(request, 'room_booking/book_room.html', {'room': room, 'error': 'Invalid booking duration. End time should be after start time.'})
        
        overlapping_bookings = Booking.objects.filter(room=room, start_time__lt=end_time, end_time__gt=start_time)
        if overlapping_bookings.exists():
            return render(request, 'room_booking/book_room.html', {'room': room, 'error': 'The room is already booked for the selected duration.'})
        
        Booking.objects.create(user=request.user, room=room, start_time=start_time, end_time=end_time)
        return redirect('/booking/list')
    
    return render(request, 'room_booking/book_room.html', {'room': room})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'room_booking/booking_list.html', {'bookings': bookings})

@login_required
def approve_booking(request):
    booking_id = request.GET.get('booking_id')
    if booking_id:
        booking = Booking.objects.get(pk=booking_id)
        booking.status = 'approved'
        booking.save()

        # Send email to the user
        subject = 'Booking Approved'
        message = f'Your booking for {booking.room} has been approved.'
        from_email = 'your_email@example.com'  # Update with your email address
        to_email = booking.user.email
        send_mail(subject, message, from_email, [to_email])

    return redirect('/booking/dashboard/')

@login_required
def reject_booking(request):
    booking_id = request.GET.get('booking_id')
    if booking_id:
        booking = Booking.objects.get(pk=booking_id)
        booking.status = 'rejected'
        booking.save()
    return redirect('/booking/dashboard/')

@login_required
def booking_dashboard(request):
    bookings = Booking.objects.filter(status='pending')
    return render(request, 'room_booking/booking_dashboard.html', {'bookings': bookings})

def admin_room_list(request):
    rooms = Room.objects.all()
    return render(request, 'room_booking/admin/room_list.html', {'rooms': rooms})

def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app_booking:admin_room_list')
    else:
        form = RoomForm()
    return render(request, 'room_booking/admin/add_room.html', {'form': form})

def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('app_booking:admin_room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'room_booking/admin/edit_room.html', {'form': form})

def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        room.delete()
        return redirect('app_booking:admin_room_list')
    return render(request, 'room_booking/admin/delete_room.html', {'room': room})