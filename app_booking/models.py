from django.db import models
from django.conf import settings



class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('conference', 'Conference'),
        ('meeting', 'Meeting'),
        ('classroom', 'Classroom'),
    )

    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='conference') 

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings') 
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    seats_booked = models.IntegerField(default=1)  # Assuming default is 1 seat

    def __str__(self):
        return f'{self.room} - {self.start_time} to {self.end_time}'
