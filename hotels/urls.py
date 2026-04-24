# hotels/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, map_view, hotel_detail_page

# Router yaratamiz
router = DefaultRouter()

# HotelViewSet-ni 'hotels' yo'li bilan ro'yxatdan o'tkazamiz
router.register(r'hotels', HotelViewSet, basename='hotel')

urlpatterns = [
    # API yo'llari /api/ prefiksi ostida ishlaydi
    path('api/', include(router.urls)),
    path('map/', map_view, name='hotel-map'),
    path('hotels/<int:pk>/', hotel_detail_page, name='hotel-detail'),
]