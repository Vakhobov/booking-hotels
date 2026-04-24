import requests
import time
from .models import Hotel

class OSMHotelSyncService:
    def __init__(self):
        # Asosiy server ishlamasa, zaxira serverlar ro'yxati
        self.mirrors = [
            "https://overpass.kumi.systems/api/interpreter",
            "https://overpass-api.de/api/interpreter",
            "https://lz4.overpass-api.de/api/interpreter"
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://overpass-turbo.eu",
            "Referer": "https://overpass-turbo.eu/"
        }

    def sync_tashkent_hotels(self):
        query = """
        [out:json][timeout:60];
        area["name:en"="Tashkent"]->.searchArea;
        (
          node["tourism"="hotel"](area.searchArea);
          way["tourism"="hotel"](area.searchArea);
          relation["tourism"="hotel"](area.searchArea);
        );
        out center;
        """
        
        data = None
        for url in self.mirrors:
            try:
                print(f"Ulanishga urinish: {url}")
                # GET emas, POST orqali yuboramiz
                response = requests.post(url, data={'data': query}, headers=self.headers, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    break
                else:
                    print(f"Server {url} xatolik berdi: {response.status_code}")
            except Exception as e:
                print(f"Ulanib bo'lmadi {url}: {e}")
                continue

        if not data:
            print("Barcha serverlar rad etdi. 2-yo'lga (Manual) o'tamiz.")
            return 0

        total_created = 0
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            lat = element.get('lat') or element.get('center', {}).get('lat')
            lon = element.get('lon') or element.get('center', {}).get('lon')
            
            if not lat or not lon: continue

            obj, created = Hotel.objects.update_or_create(
                yandex_id=str(element.get('id')), 
                defaults={
                    "name": tags.get('name') or tags.get('name:en') or 'Nomsiz mehmonxona',
                    "address": tags.get('addr:street', 'Manzil yo\'q'),
                    "phone": tags.get('phone') or tags.get('contact:phone') or "Mavjud emas",
                    "latitude": lat,
                    "longitude": lon,
                }
            )
            if created: total_created += 1
            
        return total_created




























# import requests
# import os
# import logging
# from django.conf import settings
# from .models import Hotel

# # Setting up logging so we can see what's happening in production
# logger = logging.getLogger(__name__)

# class YandexHotelSyncService:
#     def __init__(self):
#         self.api_key = os.getenv('YANDEX_API_KEY')
#         self.base_url = "https://search-maps.yandex.ru/v1/"
#         self.tashkent_coords = "69.2401,41.2995" # Longitude, Latitude
#         self.span = "0.3,0.3" # Area coverage

#     def sync_tashkent_hotels(self, limit=100):
#         """
#         Fetches hotels from Yandex and saves them to the DB.
#         Includes pagination to get more than the 50-result limit.
#         """
#         skip = 0
#         total_created = 0
        
#         while skip < limit:
#             params = {
#                 "apikey": self.api_key,
#                 "text": "hotels in Tashkent",
#                 "lang": "en_US",
#                 "type": "biz",
#                 "ll": self.tashkent_coords,
#                 "spn": self.span,
#                 "results": 50, # Max per request
#                 "skip": skip
#             }

#             try:
#                 response = requests.get(self.base_url, params=params, timeout=10)
#                 response.raise_for_status()
#                 data = response.json()
#             except Exception as e:
#                 logger.error(f"Failed to fetch data from Yandex: {e}")
#                 break

#             features = data.get('features', [])
#             if not features:
#                 break

#             for feature in features:
#                 meta = feature['properties'].get('CompanyMetaData', {})
#                 coords = feature['geometry']['coordinates'] # [Lon, Lat]

#                 # Extracting phone safely
#                 phones = meta.get('Phones', [])
#                 phone_num = phones[0].get('formatted') if phones else None

#                 # Non-MVP: update_or_create handles data updates automatically
#                 obj, created = Hotel.objects.update_or_create(
#                     yandex_id=meta.get('id'),
#                     defaults={
#                         "name": meta.get('name'),
#                         "address": meta.get('address'),
#                         "city": "Tashkent",
#                         "phone": phone_num,
#                         "latitude": coords[1],
#                         "longitude": coords[0],
#                     }
#                 )
#                 if created:
#                     total_created += 1

#             skip += 50
#             logger.info(f"Processed {skip} results...")

#         return total_created