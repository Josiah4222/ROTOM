import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import Milestone

# Define the milestones
milestones_data = [
    {
        'year': '2017',
        'title': 'Foundations of Service',
        'description': 'We launched our mission in Bishoftu by providing home-based care to 39 seniors, operating from a dedicated home office and utilizing the Genesis Farm Hall through the generosity of Mr. Behailu, while Mr. Israel Zelalem provided essential transportation services.',
        'image': 'images/2017.jpg',
        'order': 1,
        'position': 'left',
        'is_active': True
    },
    {
        'year': '2018',
        'title': 'A Strategic Leap',
        'description': 'We expanded our impact by transitioning into our own rented facility, where we opened our first residential center to provide 24/7 comprehensive care for 10 seniors while simultaneously launching a support program for 31 grandchildren of our beneficiaries.',
        'image': 'images/2018.jpg',
        'order': 2,
        'position': 'right',
        'is_active': True
    },
    {
        'year': '2019',
        'title': 'Milestones and Joy',
        'description': 'We proudly celebrated a significant educational milestone with the graduation of our first five supported grandchildren.',
        'image': 'images/2019.jpg',
        'order': 3,
        'position': 'left',
        'is_active': True
    },
    {
        'year': '2021',
        'title': 'Scaling Impact',
        'description': 'We significantly enhanced our operational capacity and outreach capabilities by purchasing our first organizational vehicle to support the center\'s logistics.',
        'image': 'images/2021.jpg',
        'order': 4,
        'position': 'right',
        'is_active': True
    },
    {
        'year': '2023',
        'title': 'Resource Mobilization',
        'description': 'We successfully executed our first major outreach campaign, raising 30.8% of our funding in cash from local sources and establishing a formal volunteer team of 50 dedicated members.',
        'image': 'images/2023.jpg',
        'order': 5,
        'position': 'left',
        'is_active': True
    },
    {
        'year': '2024',
        'title': 'Institutional Recognition',
        'description': 'In a landmark gesture of support, the Bishoftu City Administration provided us with a rent-free center and honored our impact by awarding us the "Outstanding Citizenship" award for our commitment to community service.',
        'image': 'images/2024.jpg',
        'order': 6,
        'position': 'right',
        'is_active': True
    },
    {
        'year': '2026',
        'title': 'Modernization & Digital Presence',
        'description': 'We are currently enhancing our internal excellence by developing a comprehensive NGO management system and building our official website—a major digital milestone being made possible through the expertise of two dedicated volunteers.',
        'image': 'images/2026.jpg',
        'order': 7,
        'position': 'left',
        'is_active': True
    }
]

# Clear existing milestones
Milestone.objects.all().delete()
print("Cleared existing milestones")

# Add new milestones
for data in milestones_data:
    milestone = Milestone.objects.create(**data)
    print(f"Added milestone: {milestone.year} - {milestone.title}")

print(f"\nSuccessfully added {len(milestones_data)} milestones!")
