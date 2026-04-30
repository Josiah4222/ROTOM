from django.core.management.base import BaseCommand
from rotom.models import Story


class Command(BaseCommand):
    help = 'Populate the database with existing transformation stories'

    def handle(self, *args, **kwargs):
        stories_data = [
            {
                'name': 'Aboye Waqjira',
                'title': 'A Journey from Streets to Dignity',
                'tag': 'Miraculous Recovery',
                'date_info': 'Joined May 27, 2018',
                'location_info': 'ROTOM Center',
                'content': '''When Gash Aboye Waqjira first came to ROTOM in 2018, he was broken. A car accident had left him unable to walk, and mental illness had stolen his memories. This former farmer had been wandering the streets of Bishoftu, and would lash out at anyone trying to help him.

Our staff never gave up. Through medical care and psychotherapy, something miraculous happened. In just six weeks, Aboye was walking again - defying doctors who said he'd need surgery. Our social worker Fasika Zewdu (RIP) worked tirelessly with him every day, helping him regain not just his mobility but his dignity.

Today, Aboye helps care for other seniors at our center. "Who makes the birds fly, feeds them, and lets them live? God! He who created us? Only God! Thanks to God I can now walk and care for myself," he says with deep gratitude and a smile that lights up the room.''',
                'image_1': 'images/Gash aboy before.jpg',
                'image_1_label': 'Before',
                'image_2': 'images/myindex.jpg',
                'image_2_label': 'After',
                'image_3': 'images/helpingothers.jpg',
                'image_3_label': 'Helping Others',
                'stat_1_number': '6',
                'stat_1_text': 'Weeks to Walk',
                'stat_2_number': '100%',
                'stat_2_text': 'Independence',
                'stat_3_number': 'Miracle',
                'stat_3_text': 'Recovery',
                'order': 1,
                'layout': 'reverse',
                'published': True,
            },
            {
                'name': 'Nigatu Belachew',
                'title': 'A Life Honored',
                'tag': 'Final Dignity',
                'date_info': 'Found March 22, 2024',
                'location_info': 'Church Yard, Bishoftu',
                'content': '''Senior Nigatu Belachew, about 70 years old, had survived on the streets for over 30 years with no family. When we found him near a church yard in March 2024, he had severe wounds, was bleeding, and had a persistent cough.

We took him in, gave him a bath, and rushed him to the hospital. As he recovered, his true personality emerged - peaceful, respectful, and surprisingly humorous. When his health declined in October, he received full care until he peacefully passed away.

His final words still echo in our hearts: "Why do you care for a person who is going to die? Your organization is a true God's place. May God bless ROTOM Ethiopia for eternity. I don't have anything to give back."''',
                'image_1': 'images/negebefore.jpg',
                'image_1_label': 'Before',
                'image_2': 'images/negeafter.png',
                'image_2_label': 'After',
                'image_3': 'images/negecare.jpg',
                'image_3_label': 'Care',
                'stat_1_number': '30+',
                'stat_1_text': 'Years on Streets',
                'stat_2_number': '1 Year+',
                'stat_2_text': 'Months of Care',
                'stat_3_number': 'Dignity',
                'stat_3_text': 'Restored',
                'order': 2,
                'layout': 'normal',
                'published': True,
            },
            {
                'name': 'Shaka Feysa',
                'title': 'Rediscovering Purpose Through Art',
                'tag': 'Artist & Visionary',
                'date_info': 'Found 2024',
                'location_info': 'Age 78',
                'content': '''Shaka Feysa, about 78 years old, was found on the street in 2024. This former soldier and farmer had a childhood passion for drawing - as a young boy herding cows, he would sketch on his lap with a stick, sparking his lifelong love for art.

After joining our center, Shaka was treated for a complex colon condition and recovered well. One day, he surprised us by gifting a beautiful drawing of a basket and wheat on rough paper, revealing his hidden artistic talent. We immediately enrolled him in art school.

In September, Shaka graduated from art school and found new purpose in life. He now creates business concepts for ROTOM through his artwork and always blesses our organization, saying we "gave him back his age."

"After receiving care at ROTOM, I discovered my passion for painting. My art now tells the story of me. This journey has transformed my life and given me a purpose. I wish to live long and be useful for ROTOM," Shaka says with pride.''',
                'image_1': 'images/shaqabefore.jpg',
                'image_1_label': 'Before',
                'image_2': 'images/shaqaafter.png',
                'image_2_label': 'After',
                'image_3': 'images/shaqapainting.jpg',
                'image_3_label': 'Artwork',
                'stat_1_number': '78',
                'stat_1_text': 'Years Old',
                'stat_2_number': 'Art',
                'stat_2_text': 'School Graduate',
                'stat_3_number': 'New',
                'stat_3_text': 'Purpose Found',
                'order': 3,
                'layout': 'reverse',
                'published': True,
            },
            {
                'name': 'Jemanesh',
                'title': "Jemanesh's Dream Come True",
                'tag': 'Home Transformation',
                'date_info': 'Transformed 2024',
                'location_info': 'Bishoftu',
                'content': '''Jemanesh had been living in an old, deteriorating house when ROTOM Ethiopia brought incredible news. Through generous supporters, her entire home would be completely renovated and furnished with a bed, sofa, and furniture.

"My home looks like a palace. I never expected I would have a house and would be equal to other people. Now I am living as a human being, thank God," Jemanesh says with overwhelming gratitude.

Her heartfelt message continues: "I want to thank Hawi and her coworkers. I am going to receive an Ethiopian New Year in my new house. May God provide more than you provide for me. Peace and Health Be With You."''',
                'image_1': 'images/jemanesh.jpg',
                'image_1_label': 'Before',
                'image_2': 'images/jemaneshafter.jpg',
                'image_2_label': 'After',
                'image_3': 'images/Jemaneshcenter.jpg',
                'image_3_label': 'At Center',
                'stat_1_number': 'Complete',
                'stat_1_text': 'Renovation',
                'stat_2_number': 'New',
                'stat_2_text': 'Dignity',
                'stat_3_number': 'Palace',
                'stat_3_text': 'Home',
                'order': 4,
                'layout': 'normal',
                'published': True,
            },
            {
                'name': 'Zebua Fikre',
                'title': 'From Despair to Dignity',
                'tag': 'Complete Healing',
                'date_info': 'Joined ROTOM',
                'location_info': 'Age 60+',
                'content': '''For forty years, Zebua Fikre lived in a one-room mud house with a leaky roof and dusty floor, renting from the government. She had only old beddings, no kitchen, no bathroom, and used a shared latrine. Her life was marked by profound losses - her six-month-old daughter's death and later discovering she was HIV positive.

The diagnosis brought stigma from relatives, neighbors, and friends. Only her husband stood by her until he unexpectedly passed away twenty years ago. Zebua became bedridden, unable to continue her casual work, facing each day alone with her pain and burden.

When Zebua joined ROTOM Ethiopia, everything changed. She received free medical treatment, monthly food support, regular home visits, and most importantly, a safe, clean, and secure home. She found fellowship with other ROTOM seniors and regained her confidence.

"I feel like I'm healed physically, mentally and emotionally. Now I can invite my friends confidently. Thank you very much for your help, may God bless you more and more," Zebua says with renewed hope and dignity.''',
                'image_1': 'images/zebuabefore.jpg',
                'image_1_label': 'Before',
                'image_2': 'images/zebuaafter.jpg',
                'image_2_label': 'After',
                'image_3': 'images/zebuanewhome.jpg',
                'image_3_label': 'New Home',
                'stat_1_number': '40',
                'stat_1_text': 'Years Struggling',
                'stat_2_number': 'Complete',
                'stat_2_text': 'Healing',
                'stat_3_number': 'New',
                'stat_3_text': 'Confidence',
                'order': 5,
                'layout': 'reverse',
                'published': True,
            },
        ]

        for story_data in stories_data:
            story, created = Story.objects.get_or_create(
                name=story_data['name'],
                defaults=story_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created story: {story.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Story already exists: {story.name}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully populated {len(stories_data)} stories!'))
