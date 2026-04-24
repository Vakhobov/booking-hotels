from django.core.management.base import BaseCommand
from hotels.services import OSMHotelSyncService # OSM xizmatini chaqiramiz

class Command(BaseCommand):
    help = 'Syncs hotel data from OpenStreetMap to the local database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("OSM orqali mehmonxonalarni yuklash boshlandi..."))
        
        service = OSMHotelSyncService()
        count = service.sync_tashkent_hotels()
        
        self.stdout.write(self.style.SUCCESS(f"Muvaffaqiyatli yakunlandi! {count} ta yangi mehmonxona qo'shildi."))