from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Day(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class InterestCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class VolunteerProfile(models.Model):
    TIME_CHOICES = [
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
    ]
    
    EDUCATION_CHOICES = [
        ('high_school', 'High School'),
        ('associate_degree', 'Associate Degree'),
        ('bachelor_degree', 'Bachelor Degree'),
        ('master_degree', 'Master Degree'),
        ('doctorate', 'Doctorate'),
        ('other', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=20, unique=True)
    education_level = models.CharField(max_length=50, choices=EDUCATION_CHOICES, default='high_school')
    days_available = models.ManyToManyField(Day, blank=True)
    times_available = models.CharField(max_length=50, choices=TIME_CHOICES, default='morning')
    interests = models.ManyToManyField(InterestCategory, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Added this field

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-event_date']  # Sort by newest event first


class PreviousEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)  # Added description field
    event_date = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/')
    created_at = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        ordering = ['-created_at']

        
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tx_ref = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.tx_ref} - {self.status}"
    


class FeedingRegistration(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast / ቁርስ'),
        ('lunch', 'Lunch / ምሳ'),
        ('dinner', 'Dinner / እራት'),
    ]

    LOCATION_CHOICES = [
        ('addis_ababa', 'Addis Ababa / አዲስ አበባ'),
        ('bishoftu', 'Bishoftu / ቢሾፍቱ'),
        ('adama', 'Adama / አዳማ'),
        ('mojo', 'Mojo / ሞጆ'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    preferred_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.get_meal_type_display()} at {self.get_location_display()}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email