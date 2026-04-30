from django.core.management.base import BaseCommand
from rotom.models import Milestone

class Command(BaseCommand):
    help = 'Populate milestones from static data'

    def handle(self, *args, **kwargs):
        milestones_data = [
            {
                'year': '2017',
                'title': 'Our Beginning',
                'description': 'Reach One Touch One Mission (ROTOM) Ethiopia was founded with a passion for positive change through acts of kindness. Officially registered as a non-profit charitable organization (Civil Society Organization Certificate #3764), our headquarters is in Bishoftu, Ethiopia.',
                'image': 'images/OurBeginning.jpg',
                'order': 1,
                'position': 'left'
            },
            {
                'year': '2018',
                'title': 'Expanding Our Reach',
                'description': 'We expanded our efforts by renting a facility near Ziquala behind Gold Mark Hotel. This allowed us to introduce two additional programs: 24/7 care for 10 seniors without homes and educational support for 35 young girls pursuing higher education.',
                'image': 'images/expanding.jpg',
                'order': 2,
                'position': 'right'
            },
            {
                'year': '2023',
                'title': 'New Chapter',
                'description': 'In January 2023, we secured a new location provided by the Bishoftu city administration, allowing us to continue our vital work with seniors, as well as their grandchildren and other beneficiaries.',
                'image': 'images/jemaneshafter.jpg',
                'order': 3,
                'position': 'left'
            }
        ]

        for data in milestones_data:
            milestone, created = Milestone.objects.get_or_create(
                year=data['year'],
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'image': data['image'],
                    'order': data['order'],
                    'position': data['position'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created milestone: {data["year"]} - {data["title"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Milestone already exists: {data["year"]} - {data["title"]}'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal milestones in database: {Milestone.objects.count()}'))
