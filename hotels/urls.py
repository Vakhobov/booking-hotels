# hotels/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HotelViewSet, map_view

# Router yaratamiz
router = DefaultRouter()

# HotelViewSet-ni 'hotels' yo'li bilan ro'yxatdan o'tkazamiz
router.register(r'hotels', HotelViewSet, basename='hotel')

urlpatterns = [
    # Router orqali generatsiya qilingan barcha URL-larni ulaymiz
    path('', include(router.urls)),
    path('map/', map_view, name='hotel-map'),
]