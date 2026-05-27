from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .utils import compress_image


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

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    title_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of title (optional)")
    summary = models.CharField(max_length=300, help_text="Brief description shown on the blog page")
    summary_am = models.CharField(max_length=300, blank=True, help_text="Amharic translation of summary (optional)")
    content = models.TextField(help_text="Write naturally - no HTML needed")
    content_am = models.TextField(blank=True, help_text="Amharic translation of content (optional)")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    published = models.BooleanField(default=False, help_text="Check to make visible on blog page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Event(models.Model):
    title = models.CharField(max_length=200)
    title_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of title (optional)")
    description = models.TextField()
    description_am = models.TextField(blank=True, help_text="Amharic translation of description (optional)")
    event_date = models.DateTimeField(db_index=True)
    image = models.ImageField(upload_to='event_images/')
    story_poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-event_date']


class PreviousEvent(models.Model):
    title = models.CharField(max_length=200)
    title_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of title (optional)")
    description = models.TextField(null=True, blank=True)
    description_am = models.TextField(blank=True, help_text="Amharic translation of description (optional)")
    event_date = models.DateTimeField()
    image = models.ImageField(upload_to='event_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

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
    name_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of name (optional)")
    description = models.TextField(blank=True, help_text="Brief description of the renovation")
    description_am = models.TextField(blank=True, help_text="Amharic translation of description (optional)")
    before_image = models.ImageField(upload_to='renovations/')
    after_image = models.ImageField(upload_to='renovations/')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Compress both images before saving
        if self.before_image:
            self.before_image = compress_image(self.before_image)
        if self.after_image:
            self.after_image = compress_image(self.after_image)
        super().save(*args, **kwargs)

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
    name_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of name (optional)")
    title = models.CharField(max_length=300, help_text="Story title (e.g., A Journey from Streets to Dignity)")
    title_am = models.CharField(max_length=300, blank=True, help_text="Amharic translation of title (optional)")
    tag = models.CharField(max_length=100, help_text="Story tag (e.g., Miraculous Recovery)")
    tag_am = models.CharField(max_length=100, blank=True, help_text="Amharic translation of tag (optional)")
    date_info = models.CharField(max_length=100, help_text="Date information (e.g., Joined May 27, 2018)")
    date_info_am = models.CharField(max_length=100, blank=True, help_text="Amharic translation of date info (optional)")
    location_info = models.CharField(max_length=100, help_text="Location information (e.g., ROTOM Center)")
    location_info_am = models.CharField(max_length=100, blank=True, help_text="Amharic translation of location info (optional)")
    content = models.TextField(help_text="Full story content - use paragraphs separated by blank lines")
    content_am = models.TextField(blank=True, help_text="Amharic translation of content (optional)")
    quote = models.TextField(default="", help_text="Featured quote from the story (e.g., 'I never thought I would walk again.')")
    quote_am = models.TextField(blank=True, help_text="Amharic translation of quote (optional)")
    image_1 = models.ImageField(upload_to='stories/', help_text="First image (Before)")
    image_1_label = models.CharField(max_length=50, default="Before")
    image_1_label_am = models.CharField(max_length=50, blank=True, help_text="Amharic label (optional)")
    image_2 = models.ImageField(upload_to='stories/', help_text="Second image (After)")
    image_2_label = models.CharField(max_length=50, default="After")
    image_2_label_am = models.CharField(max_length=50, blank=True, help_text="Amharic label (optional)")
    image_3 = models.ImageField(upload_to='stories/', help_text="Third image")
    image_3_label = models.CharField(max_length=50, default="At Center")
    image_3_label_am = models.CharField(max_length=50, blank=True, help_text="Amharic label (optional)")
    stat_1_number = models.CharField(max_length=20, help_text="First statistic number (e.g., 6)")
    stat_1_text = models.CharField(max_length=50, help_text="First statistic text (e.g., Weeks to Walk)")
    stat_1_text_am = models.CharField(max_length=50, blank=True, help_text="Amharic translation (optional)")
    stat_2_number = models.CharField(max_length=20, help_text="Second statistic number")
    stat_2_text = models.CharField(max_length=50, help_text="Second statistic text")
    stat_2_text_am = models.CharField(max_length=50, blank=True, help_text="Amharic translation (optional)")
    stat_3_number = models.CharField(max_length=20, help_text="Third statistic number")
    stat_3_text = models.CharField(max_length=50, help_text="Third statistic text")
    stat_3_text_am = models.CharField(max_length=50, blank=True, help_text="Amharic translation (optional)")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    layout = models.CharField(max_length=20, choices=[('normal', 'Images Left'), ('reverse', 'Images Right')], default='normal')
    published = models.BooleanField(default=True, help_text="Check to display on stories page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        from django.core.files.uploadedfile import InMemoryUploadedFile
        if self.image_1 and isinstance(self.image_1.file, InMemoryUploadedFile):
            self.image_1 = compress_image(self.image_1)
        if self.image_2 and isinstance(self.image_2.file, InMemoryUploadedFile):
            self.image_2 = compress_image(self.image_2)
        if self.image_3 and isinstance(self.image_3.file, InMemoryUploadedFile):
            self.image_3 = compress_image(self.image_3)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.title}"

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Stories"


class DonationPackage(models.Model):
    title = models.CharField(max_length=200, help_text="Package title (e.g., Home Care Support)")
    title_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of title (optional)")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount in ETB")
    description = models.CharField(max_length=300, help_text="Short description (e.g., Supports a senior living at home for one month)")
    description_am = models.CharField(max_length=300, blank=True, help_text="Amharic translation of description (optional)")
    features = models.TextField(help_text="List of features, one per line")
    features_am = models.TextField(blank=True, help_text="Amharic translation of features, one per line (optional)")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display on donation page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ETB"

    def get_features_list(self):
        """Return features as a list"""
        return [f.strip() for f in self.features.split('\n') if f.strip()]

    def get_features_list_am(self):
        """Return Amharic features as a list"""
        return [f.strip() for f in self.features_am.split('\n') if f.strip()]

    class Meta:
        ordering = ['order', 'amount']
        verbose_name_plural = "Donation Packages"


class Champion(models.Model):
    name = models.CharField(max_length=200, help_text="Student's name (e.g., Meron Tadesse)")
    role = models.CharField(max_length=200, help_text="Role/Status (e.g., University Student, Age 19)")
    role_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of role (optional)")
    quote = models.TextField(help_text="Their testimonial/story")
    quote_am = models.TextField(blank=True, help_text="Amharic translation of quote (optional)")
    image = models.ImageField(upload_to='champions/', help_text="Main photo")
    years_supported = models.CharField(max_length=50, help_text="e.g., 5 or 3-5")
    achievement = models.CharField(max_length=100, help_text="e.g., 1st In Family to University or Top 5% Class Ranking")
    achievement_am = models.CharField(max_length=100, blank=True, help_text="Amharic translation of achievement (optional)")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    layout = models.CharField(max_length=20, choices=[('normal', 'Image Left'), ('reverse', 'Image Right')], default='normal')
    is_active = models.BooleanField(default=True, help_text="Check to display on champions page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.role}"

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Champions"


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, help_text="Image title (e.g., Girls Empowerment)")
    title_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of title (optional)")
    caption = models.TextField(blank=True, help_text="Image caption/description (optional)")
    caption_am = models.TextField(blank=True, help_text="Amharic translation of caption (optional)")
    image = models.ImageField(upload_to='gallery/', help_text="Gallery photo")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display in gallery")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Gallery Images"

class Milestone(models.Model):
    year = models.CharField(max_length=10, help_text="Year of the milestone (e.g., 2017)")
    title = models.CharField(max_length=200, help_text="Milestone title")
    title_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of title (optional)")
    description = models.TextField(help_text="Detailed description of the milestone")
    description_am = models.TextField(blank=True, help_text="Amharic translation of description (optional)")
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

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.year} - {self.title}"

    class Meta:
        ordering = ['order', 'year']
        verbose_name_plural = "Milestones"

class TeamMember(models.Model):
    name = models.CharField(max_length=200, help_text="Team member's full name")
    name_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of name (optional)")
    position = models.CharField(max_length=200, help_text="Job title/position (e.g., Director, Social Worker)")
    position_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of position (optional)")
    image = models.ImageField(upload_to='team/', help_text="Team member photo")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display on website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Team Members"

class CenterPhoto(models.Model):
    title = models.CharField(max_length=200, help_text="Photo title (e.g., Dining Room)")
    title_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of title (optional)")
    description = models.TextField(help_text="Brief description of the space")
    description_am = models.TextField(blank=True, help_text="Amharic translation of description (optional)")
    image = models.ImageField(upload_to='center/', help_text="Center photo")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display in gallery")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

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
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image, max_width=1920, max_height=200, quality=90)
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
    description_am = models.TextField(blank=True, help_text="Amharic translation of description (optional)")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display in partners section")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Compress logo before saving (smaller size for logos)
        if self.logo:
            self.logo = compress_image(self.logo, max_width=400, max_height=400, quality=90)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Partners"


class SiteContent(models.Model):
    """
    Stores editable static text content for each page section.
    Use page + key to uniquely identify a piece of content.
    """
    PAGE_CHOICES = [
        ('navbar', 'Navbar'),
        ('home', 'Home Page'),
        ('about', 'About Us Page'),
        ('centerbased', 'Center-Based Care Page'),
        ('homebased', 'Home-Based Care Page'),
        ('champions', 'Champions / Grandchildren Page'),
        ('stories', 'Stories Page'),
        ('takeaction', 'Take Action Page'),
        ('volunteer', 'Volunteer Page'),
    ]

    page = models.CharField(max_length=50, choices=PAGE_CHOICES, db_index=True)
    key = models.CharField(max_length=100, db_index=True, help_text="Internal identifier (e.g. hero_title, hero_subtitle)")
    label = models.CharField(max_length=200, help_text="Human-readable label shown in the dashboard")
    value = models.TextField(blank=True, help_text="The text content displayed on the website (English)")
    value_am = models.TextField(blank=True, default='', help_text="Amharic translation (optional)")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('page', 'key')
        ordering = ['page', 'key']
        verbose_name = "Site Content"
        verbose_name_plural = "Site Content"

    def __str__(self):
        return f"[{self.get_page_display()}] {self.label}"

    @classmethod
    def get(cls, page, key, default=''):
        """Retrieve a content value with a fallback default."""
        try:
            return cls.objects.get(page=page, key=key).value
        except cls.DoesNotExist:
            return default


class Testimonial(models.Model):
    name = models.CharField(max_length=200, help_text="Person's name (e.g., John Doe)")
    name_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of name (optional)")
    role = models.CharField(max_length=200, help_text="Role/Title (e.g., Volunteer, Donor, Partner)")
    role_am = models.CharField(max_length=200, blank=True, help_text="Amharic translation of role (optional)")
    quote = models.TextField(help_text="Their testimonial/feedback")
    quote_am = models.TextField(blank=True, help_text="Amharic translation of quote (optional)")
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True, help_text="Photo (optional)")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display on website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Compress image before saving
        if self.image:
            self.image = compress_image(self.image, max_width=800, max_height=800, quality=90)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.role}"

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Testimonials"


class VolunteerGallery(models.Model):
    title = models.CharField(max_length=200, help_text="Image title or description")
    image = models.ImageField(upload_to='volunteer_gallery/', help_text="Volunteer activity photo")
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")
    is_active = models.BooleanField(default=True, help_text="Check to display in gallery")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image, max_width=1200, max_height=1200, quality=85)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name_plural = "Volunteer Gallery"
