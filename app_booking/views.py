import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Booking

# @login_required
def room_list(request):
    query = request.GET.get('search')
    if query:
        rooms = Room.objects.filter(room__name__icontains=query)
    else:
        rooms = Room.objects.all()
    return render(request, 'room_booking/room_list.html', {'rooms': rooms})

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    print(room_id)
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if start_time >= end_time:
            return render(request, 'room_booking/book_room.html', {'room': room, 'error': 'Invalid booking duration. End time should be after start time.'})
        overlapping_bookings = Booking.objects.filter(room=room, start_time__lt=end_time, end_time__gt=start_time)
        if overlapping_bookings.exists():
            return render(request, 'room_booking/book_room.html', {'room': room, 'error': 'The room is already booked for the selected duration.'})
        Booking.objects.create(room=room, start_time=start_time, end_time=end_time)
        return redirect('/booking/list')
    return render(request, 'room_booking/book_room.html', {'room': room})


@login_required
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'room_booking/booking_list.html', {'bookings': bookings})