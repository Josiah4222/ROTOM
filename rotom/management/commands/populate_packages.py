from django.core.management.base import BaseCommand
from rotom.models import DonationPackage


class Command(BaseCommand):
    help = 'Populate the database with existing donation packages'

    def handle(self, *args, **kwargs):
        packages_data = [
            {
                'title': 'Home Care Support',
                'amount': 1800,
                'description': 'Supports a senior living at home for one month',
                'features': '''Essential food commodities
Essential hygiene items
Social outings and lunches''',
                'order': 1,
                'is_active': True,
            },
            {
                'title': 'Care Center Support',
                'amount': 4000,
                'description': 'Provides one month of care for a senior in our center',
                'features': '''Nutritious meals three times a day
Hygiene supplies
Essential healthcare support''',
                'order': 2,
                'is_active': True,
            },
            {
                'title': 'Annual Senior Support',
                'amount': 4400,
                'description': 'Provides clothing and healthcare for a senior for one year',
                'features': '''Essential clothing
Necessary healthcare support''',
                'order': 3,
                'is_active': True,
            },
            {
                'title': 'Education Support',
                'amount': 7350,
                'description': "Empowers a child's education for one year",
                'features': '''School fees (primary/secondary)
Uniforms and school supplies
Hygiene care for female students''',
                'order': 4,
                'is_active': True,
            },
        ]

        for package_data in packages_data:
            package, created = DonationPackage.objects.get_or_create(
                title=package_data['title'],
                defaults=package_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created package: {package.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Package already exists: {package.title}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully populated {len(packages_data)} donation packages!'))
