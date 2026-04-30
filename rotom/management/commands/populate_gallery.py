from django.core.management.base import BaseCommand
from rotom.models import GalleryImage

class Command(BaseCommand):
    help = 'Populate gallery images from static files'

    def handle(self, *args, **kwargs):
        gallery_data = [
            {
                'title': 'Girls Empowerment',
                'caption': 'Supporting girls through education and mentorship to build a brighter future.',
                'image': 'images/girls1.jpg',
                'order': 1
            },
            {
                'title': 'Girls Empowerment',
                'caption': 'Empowering young girls with skills and confidence for life.',
                'image': 'images/girls2.jpg',
                'order': 2
            },
            {
                'title': 'Girls Empowerment',
                'caption': 'Creating opportunities for girls to thrive and succeed.',
                'image': 'images/girls3.jpg',
                'order': 3
            },
            {
                'title': 'Girls Empowerment',
                'caption': 'Building a community of strong, educated young women.',
                'image': 'images/girls4.jpg',
                'order': 4
            },
            {
                'title': 'Girls Empowerment',
                'caption': 'Nurturing talent and potential in every young girl we support.',
                'image': 'images/girls5.jpg',
                'order': 5
            },
            {
                'title': 'Girls Empowerment',
                'caption': 'Together, transforming lives through education and care.',
                'image': 'images/girls6.jpg',
                'order': 6
            }
        ]

        for data in gallery_data:
            image, created = GalleryImage.objects.get_or_create(
                image=data['image'],
                defaults={
                    'title': data['title'],
                    'caption': data['caption'],
                    'order': data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created gallery image: {data["title"]} (Order: {data["order"]})'))
            else:
                self.stdout.write(self.style.WARNING(f'Gallery image already exists: {data["title"]}'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal gallery images in database: {GalleryImage.objects.count()}'))
