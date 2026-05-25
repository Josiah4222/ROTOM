import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import Partner

partners_map = {
    'ROTOM USA': 'partners/rotom_usa.jpg',
    'Canada Partnership': 'partners/canada.jpg',
    'GK Organization': 'partners/gk.jpg',
    'AHSAM': 'partners/ahsam.jpg',
    'Andu Foundation': 'partners/andu.jpg',
    'Alfa Organization': 'partners/alfa.jpg',
    'Beautiful World': 'partners/beautifulworld.jpg',
    'EDF': 'partners/edf.jpg',
    'Global Care': 'partners/globalcare.jpg',
    'Maranatha': 'partners/maranatha.jpg',
    'Pyramid Foundation': 'partners/pyramid.jpg'
}

for name, path in partners_map.items():
    Partner.objects.filter(name=name).update(logo=path, is_active=True)

print("Partner logos migrated and database updated successfully!")
