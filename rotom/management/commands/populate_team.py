from django.core.management.base import BaseCommand
from rotom.models import TeamMember

class Command(BaseCommand):
    help = 'Populate team members from static data'

    def handle(self, *args, **kwargs):
        team_data = [
            {
                'name': 'Hawi Belete',
                'position': 'Director',
                'image': 'images/hawi.jpg',
                'order': 1
            },
            {
                'name': 'Bizunesh Alemayehu',
                'position': 'Social Worker',
                'image': 'images/buzepro.jpg',
                'order': 2
            },
            {
                'name': 'Tigi Shambel',
                'position': 'Program Assistant',
                'image': 'images/tg.jpg',
                'order': 3
            },
            {
                'name': 'Muse Etana',
                'position': 'Nurse',
                'image': 'images/muse.jpg',
                'order': 4
            },
            {
                'name': 'Saron Tesfaye',
                'position': 'Program Manager',
                'image': 'images/saron.jpg',
                'order': 5
            }
        ]

        for data in team_data:
            member, created = TeamMember.objects.get_or_create(
                name=data['name'],
                defaults={
                    'position': data['position'],
                    'image': data['image'],
                    'order': data['order'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created team member: {data["name"]} - {data["position"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Team member already exists: {data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'\nTotal team members in database: {TeamMember.objects.count()}'))
