from django.shortcuts import render
from rest_framework import viewsets
from .models import Hotel
from .serializers import HotelDetailSerializer

class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotelDetailSerializer

    def get_queryset(self):
        queryset = Hotel.objects.all()
        
        # Brauzerdan yuborilgan xarita chegaralari (bounding box)
        min_lat = self.request.query_params.get('min_lat')
        max_lat = self.request.query_params.get('max_lat')
        min_lon = self.request.query_params.get('min_lon')
        max_lon = self.request.query_params.get('max_lon')

        if all([min_lat, max_lat, min_lon, max_lon]):
            queryset = queryset.filter(
                latitude__range=(min_lat, max_lat),
                longitude__range=(min_lon, max_lon)
            )
        return queryset


def map_view(request):
    return render(request, 'map.html')

def hotel_detail_page(request, pk):
    return render(request, 'hotel_detail.html', {'hotel_id': pk})