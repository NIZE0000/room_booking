from django.urls import path
from . import views

app_name = 'app_booking'  

urlpatterns = [
    path('rooms/', views.room_list, name='room_list'),
    path('book/<int:room_id>', views.book_room, name='book_room'),
    path('list/', views.booking_list, name='booking_list'),

    path('dashboard/', views.booking_dashboard, name='booking_dashboard'),
    path('approve/', views.approve_booking, name='approve_booking'),
    path('reject/', views.reject_booking, name='reject_booking'),

    path('admin/rooms/', views.admin_room_list, name='admin_room_list'),
    path('admin/rooms/add/', views.add_room, name='add_room'),
    path('admin/rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('admin/rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'),
]
