from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def remaining_rooms(self):
        total_bookings = self.bookings.count()
        return self.capacity - total_bookings

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings') 
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.room} - {self.start_time} to {self.end_time}'
