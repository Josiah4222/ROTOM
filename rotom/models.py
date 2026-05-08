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
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    ADDRESS_CHOICES = [
        ('addis_ababa', 'Addis Ababa'),
        ('bishoftu', 'Bishoftu'),
        ('adama', 'Adama'),
        ('debre_zeit', 'Debre Zeit'),
        ('mojo', 'Mojo'),
        ('dukem', 'Dukem'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=50, choices=ADDRESS_CHOICES, default='addis_ababa')
    education_level = models.CharField(max_length=50, choices=EDUCATION_CHOICES, default='high_school')
    days_available = models.ManyToManyField(Day, blank=True)
    times_available = models.CharField(max_length=50, choices=TIME_CHOICES, default='morning')
    interests = models.ManyToManyField(InterestCategory, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('scheduled', 'Scheduled'),
    ]
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    content = models.TextField(help_text="Newsletter content (HTML supported)")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    recipients_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300, help_text="Brief description shown on the blog page")
    content = models.TextField(help_text="Write naturally - no HTML needed")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    published = models.BooleanField(default=False, help_text="Check to make visible on blog page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField(db_index=True)
    image = models.ImageField(upload_to='event_images/')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-event_date']


class PreviousEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    event_date = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    email = models.EmailField(db_index=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        ordering = ['-created_at']


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tx_ref = models.CharField(max_length=100, unique=True, db_index=True)
    status = models.CharField(max_length=20, default='pending', db_index=True)
    email = models.EmailField(db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.tx_ref} - {self.status}"


class HouseRenovation(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the beneficiary")
    description = models.TextField(blank=True, help_text="Brief description of the renovation")
    before_image = models.ImageField(upload_to='renovations/')
    after_image = models.ImageField(upload_to='renovations/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


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


class Story(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the person (e.g., Aboye Waqjira)")
    title = models.CharField(max_length=300, help_text="Story title (e.g., A Journey from Streets to Dignity)")
    tag = models.CharField(max_length=100, help_text="Story tag (e.g., Miraculous Recovery)")
    date_info = models.CharField(max_length=100, help_text="Date information (e.g., Joined May 27, 2018)")
    location_info = models.CharField(max_length=100, help_text="Location information (e.g., ROTOM Center)")
    content = models.TextField(help_text="Full story content - use paragraphs separated by blank lines")
    image_1 = models.ImageField(upload_to='stories/', help_text="First image (Before)")
    image_1_label = models.CharField(max_length=50, default="Before")
    image_2 = models.ImageField(upload_to='stories/', help_text="Second image (After)")
    image_2_label = models.CharField(max_length=50, default="After")
    image_3 = models.ImageField(upload_to='stories/', help_text="Third image")
    image_3_label = models.CharField(max_length=50, default="At Center")
    stat_1_number = models.CharField(max_length=20, help_text="First statistic number (e.g., 6)")
    stat_1_text = models.CharField(max_length=50, help_text="First statistic text (e.g., Weeks to Walk)")
    stat_2_number = models.CharField(max_length=20, help_text="Second statistic number")
    stat_2_text = models.CharField(max_length=50, help_text="Second statistic text")
    stat_3_number = models.CharField(max_length=20, help_text="Third statistic number")
    stat_3_text = models.CharField(max_length=50, help_text="Third statistic text")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    layout = models.CharField(max_length=20, choices=[('normal', 'Images Left'), ('reverse', 'Images Right')], default='normal')
    published = models.BooleanField(default=True, help_text="Check to display on stories page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.title}"

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Stories"


class DonationPackage(models.Model):
    title = models.CharField(max_length=200, help_text="Package title (e.g., Home Care Support)")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in ETB")
    description = models.CharField(max_length=300, help_text="Short description (e.g., Supports a senior living at home for one month)")
    features = models.TextField(help_text="List of features, one per line")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display on donation page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ETB"

    def get_features_list(self):
        """Return features as a list"""
        return [f.strip() for f in self.features.split('\n') if f.strip()]

    class Meta:
        ordering = ['order', 'amount']
        verbose_name_plural = "Donation Packages"


class Champion(models.Model):
    name = models.CharField(max_length=200, help_text="Student's name (e.g., Meron Tadesse)")
    role = models.CharField(max_length=200, help_text="Role/Status (e.g., University Student, Age 19)")
    quote = models.TextField(help_text="Their testimonial/story")
    image = models.ImageField(upload_to='champions/', help_text="Main photo")
    years_supported = models.CharField(max_length=50, help_text="e.g., 5 or 3-5")
    achievement = models.CharField(max_length=100, help_text="e.g., 1st In Family to University or Top 5% Class Ranking")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    layout = models.CharField(max_length=20, choices=[('normal', 'Image Left'), ('reverse', 'Image Right')], default='normal')
    is_active = models.BooleanField(default=True, help_text="Check to display on champions page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.role}"

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Champions"


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, help_text="Image title (e.g., Girls Empowerment)")
    caption = models.TextField(help_text="Image caption/description")
    image = models.ImageField(upload_to='gallery/', help_text="Gallery photo")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display in gallery")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Gallery Images"

class Milestone(models.Model):
    year = models.CharField(max_length=10, help_text="Year of the milestone (e.g., 2017)")
    title = models.CharField(max_length=200, help_text="Milestone title")
    description = models.TextField(help_text="Detailed description of the milestone")
    image = models.ImageField(upload_to='milestones/', help_text="Milestone photo")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    position = models.CharField(
        max_length=10,
        choices=[('left', 'Left'), ('right', 'Right')],
        default='left',
        help_text="Position on timeline (alternates left/right)"
    )
    is_active = models.BooleanField(default=True, help_text="Check to display on timeline")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} - {self.title}"

    class Meta:
        ordering = ['order', 'year']
        verbose_name_plural = "Milestones"

class TeamMember(models.Model):
    name = models.CharField(max_length=200, help_text="Team member's full name")
    position = models.CharField(max_length=200, help_text="Job title/position (e.g., Director, Social Worker)")
    image = models.ImageField(upload_to='team/', help_text="Team member photo")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display on website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Team Members"

class CenterPhoto(models.Model):
    title = models.CharField(max_length=200, help_text="Photo title (e.g., Dining Room)")
    description = models.TextField(help_text="Brief description of the space")
    image = models.ImageField(upload_to='center/', help_text="Center photo")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display in gallery")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', 'title']
        verbose_name_plural = "Center Photos"


class NavbarPattern(models.Model):
    name = models.CharField(max_length=200, help_text="Pattern name (e.g., Green Ethiopian Pattern)")
    image = models.ImageField(upload_to='patterns/', help_text="Pattern image (recommended: horizontal repeating pattern)")
    height = models.IntegerField(default=60, help_text="Pattern bar height in pixels (default: 60)")
    opacity = models.DecimalField(max_digits=3, decimal_places=2, default=0.80, help_text="Pattern opacity (0.00 to 1.00, default: 0.80)")
    is_active = models.BooleanField(default=False, help_text="Check to use this pattern on the navbar (only one can be active)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {'(Active)' if self.is_active else ''}"

    def save(self, *args, **kwargs):
        # If this pattern is being set as active, deactivate all others
        if self.is_active:
            NavbarPattern.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-is_active', '-created_at']
        verbose_name_plural = "Navbar Patterns"


class Partner(models.Model):
    name = models.CharField(max_length=200, help_text="Partner organization name")
    logo = models.ImageField(upload_to='partners/', help_text="Partner logo (recommended: transparent PNG, square or landscape)")
    website = models.URLField(blank=True, help_text="Partner website URL (optional)")
    description = models.TextField(blank=True, help_text="Brief description of the partnership (optional)")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display in partners section")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Partners"
