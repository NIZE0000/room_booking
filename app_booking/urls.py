from django.urls import path
from . import views

app_name = 'app_booking'  

urlpatterns = [
    path('rooms/', views.room_list, name='room_list'),
    path('book/<int:room_id>', views.book_room, name='book_room'),
    path('list/', views.booking_list, name='booking_list'),
]
