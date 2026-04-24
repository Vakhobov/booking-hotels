# hotels/models.py
from django.db import models

class Hotel(models.Model):
    # OSM ID-lari uzun bo'lishi mumkin, 100 yetarli
    yandex_id = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    address = models.TextField()
    city = models.CharField(max_length=100, default="Tashkent")
    
    # Telefon raqamlari 50 tadan oshib ketishi mumkin (masalan: +998...; +998...)
    # Shuning uchun buni 255 qilamiz yoki TextField ishlatamiz
    phone = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='hotels/', null=True, blank=True)
    
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return self.name
    
class Room(models.Model):
    ROOM_TYPES = (
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
    )

    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Masalan: 500000.00 so'm
    is_available = models.BooleanField(default=True)
    capacity = models.IntegerField(default=2) # Necha kishilik

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"