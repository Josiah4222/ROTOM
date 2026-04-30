import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import VolunteerProfile

volunteers = VolunteerProfile.objects.all()
print(f"Total volunteers in database: {volunteers.count()}")
print("\nVolunteer List:")
print("-" * 50)
for v in volunteers:
    print(f"{v.first_name} {v.last_name} - {v.phone_number} - Age: {v.age}")
