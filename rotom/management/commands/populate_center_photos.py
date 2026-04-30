from django.core.management.base import BaseCommand
from rotom.models import CenterPhoto

class Command(BaseCommand):
    help = 'Populate center photos from static data'

    def handle(self, *args, **kwargs):
        photos_data = [
            {
                'title': 'Dining Room',
                'description': 'A comfortable space for seniors to enjoy meals together.',
                'image': 'images/dining.jpg',
                'order': 1
            },
            {
                'title': 'Elders Room',
                'description': 'Cozy and well-maintained rooms for rest and relaxation.',
                'image': 'images/centerbased.jpg',
                'order': 2
            },
            {
                'title': 'Center Kitchen',
                'description': 'A modern kitchen preparing nutritious meals daily.',
                'image': 'images/kitchen.jpg',
                'order': 3
            },
            {
                'title': 'Common Area',
                'description': 'A vibrant space for social activities and community bonding.',
                'image': 'images/common.jpg',
                'order': 4
            }
        ]

        for data in photos_data:
            photo, created = CenterPhoto.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'image': data['image'],
                    'order': data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created center photo: {data["title"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Center photo already exists: {data["title"]}'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal center photos in database: {CenterPhoto.objects.count()}'))
