# hotels/serializers.py
from rest_framework import serializers
from .models import Hotel, Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'room_type', 'price', 'is_available', 'capacity']

class HotelDetailSerializer(serializers.ModelSerializer):
    # 'rooms' bu yerda Hotel modelidagi related_name
    rooms = RoomSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'phone', 'latitude', 'longitude', 'rating', 'image', 'rooms']

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return "https://via.placeholder.com/800x400?text=No+Image" # Rasm bo'lmasa placeholder