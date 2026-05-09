import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'REACHONEETH.settings')
django.setup()

from rotom.models import NavbarPattern

# Clear existing patterns
NavbarPattern.objects.all().delete()
print("Cleared existing navbar patterns")

# Add the navbar pattern
pattern = NavbarPattern.objects.create(
    name="Green Ethiopian Pattern",
    image="images/pattern_green.png",  # Using the pattern from static/images/patterns/
    height=8,  # Height in pixels
    opacity=1.0,  # Full opacity
    is_active=True
)

print(f"Added navbar pattern: {pattern.name}")
print(f"Image: {pattern.image}")
print(f"Height: {pattern.height}px")
print(f"Opacity: {pattern.opacity}")
print("\nNavbar pattern added successfully!")
