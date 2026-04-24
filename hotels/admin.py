from django.contrib import admin
from .models import Hotel, Room 
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'latitude', 'longitude')
    search_fields = ('name', 'address', 'phone')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'capacity', 'price')
    search_fields = ('room_type',)