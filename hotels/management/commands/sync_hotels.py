from django.core.management.base import BaseCommand
from hotels.services import OSMHotelSyncService # OSM xizmatini chaqiramiz

class Command(BaseCommand):
    help = 'Belgilangan shahar bo\'yicha mehmonxonalarni yuklash'

    def add_arguments(self, parser):
        # Shahar nomini argument sifatida qo'shish
        parser.add_argument('city', type=str, help='Shahar nomi (masalan: Samarkand)')

    def handle(self, *args, **options):
        city = options['city']
        self.stdout.write(self.style.WARNING(f"{city} bo'yicha mehmonxonalarni yuklash boshlandi..."))
        
        service = OSMHotelSyncService()
        count = service.sync_hotels_by_city(city)
        
        self.stdout.write(self.style.SUCCESS(f"Tayyor! {city}dan {count} ta yangi mehmonxona qo'shildi."))