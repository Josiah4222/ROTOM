from django.core.management.base import BaseCommand
from rotom.models import Champion


class Command(BaseCommand):
    help = 'Populate the database with existing champion stories'

    def handle(self, *args, **kwargs):
        champions_data = [
            {
                'name': 'Meron Tadesse',
                'role': 'University Student, Age 19',
                'quote': '''When my grandmother became too ill to work, I thought my dreams of education were over. ROTOM Ethiopia not only paid for my school fees but gave me a mentor who believed in me. Today, I'm studying nursing at university. I want to give back to my community just like ROTOM gave to me.''',
                'image': 'images/champions.jpg',
                'years_supported': '5',
                'achievement': '1st In Family to University',
                'order': 1,
                'layout': 'normal',
                'is_active': True,
            },
            {
                'name': 'Dawit Bekele',
                'role': 'High School Graduate, Age 17',
                'quote': '''Living with my elderly grandfather, I had to choose between helping him and going to school. ROTOM's home visits and support meant I could do both. My mentor taught me time management and encouraged me when things got hard. I just graduated top of my class!''',
                'image': 'images/centerbased.jpg',
                'years_supported': '3',
                'achievement': 'Top 5% Class Ranking',
                'order': 2,
                'layout': 'reverse',
                'is_active': True,
            },
            {
                'name': 'Meklit Kibret',
                'role': 'Diploma Graduate in Automotive Servicing, Operation Management & ICT, 2021',
                'quote': '''Orphaned at a young age, Meklit was raised by her grandmother Zewde from age five. After completing Grade 10, she was forced to pause her education and work as a janitor to survive. In 2018, ROTOM Ethiopia and its partner Beautiful World Canada stepped in — enabling her to return to school and graduate in 2021.

Today, Meklit works as a skilled mechanic at the Bishoftu Automotive Engineering Industry and is pursuing a degree in Mechanical Engineering.

"I don't have words to express how grateful I am. You have changed my life and future, moving me from a place of survival to one of professional ambition. I am a different person now — transformed through education, training, and mentorship. I will be an inspiration to others and will give care to orphaned children in my community."''',
                'image': 'images/meklit1.jpg',
                'years_supported': '4',
                'achievement': '1st In Family to Attend College',
                'order': 3,
                'layout': 'normal',
                'is_active': True,
            },
        ]

        for champion_data in champions_data:
            champion, created = Champion.objects.get_or_create(
                name=champion_data['name'],
                defaults=champion_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created champion: {champion.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Champion already exists: {champion.name}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully populated {len(champions_data)} champion stories!'))
