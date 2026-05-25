from django import forms
from rotom.models import (
    Event, PreviousEvent, Newsletter, BlogPost, Story, DonationPackage,
    Champion, GalleryImage, Milestone, TeamMember, CenterPhoto, Partner,
    Testimonial, HouseRenovation
)

# ── Shared widget helpers ─────────────────────────────────────────────────────

def text(placeholder='', **kw):
    return forms.TextInput(attrs={'class': 'form-control', 'placeholder': placeholder, **kw})

def textarea(placeholder='', rows=4, **kw):
    return forms.Textarea(attrs={'class': 'form-control', 'rows': rows, 'placeholder': placeholder, **kw})

def file_input():
    return forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'})

def number(placeholder='0'):
    return forms.NumberInput(attrs={'class': 'form-control', 'placeholder': placeholder})

def select():
    return forms.Select(attrs={'class': 'form-control'})

def checkbox():
    return forms.CheckboxInput(attrs={'class': 'form-check-input'})

AM_NOTE = ' (አማርኛ — optional)'


# ── Event ─────────────────────────────────────────────────────────────────────

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'title_am', 'description', 'description_am', 'event_date', 'image']
        widgets = {
            'title': text('Event Title'),
            'title_am': text('የዝግጅቱ ርዕስ'),
            'description': textarea('Event Description'),
            'description_am': textarea('የዝግጅቱ መግለጫ'),
            'event_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title (English)',
            'title_am': 'Title' + AM_NOTE,
            'description': 'Description (English)',
            'description_am': 'Description' + AM_NOTE,
            'event_date': 'Date & Time',
            'image': 'Event Image',
        }


class PreviousEventForm(forms.ModelForm):
    class Meta:
        model = PreviousEvent
        fields = ['title', 'title_am', 'description', 'description_am', 'event_date', 'image']
        widgets = {
            'title': text('Event Title'),
            'title_am': text('የዝግጅቱ ርዕስ'),
            'description': textarea('Event Description'),
            'description_am': textarea('የዝግጅቱ መግለጫ'),
            'event_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title (English)',
            'title_am': 'Title' + AM_NOTE,
            'description': 'Description (English)',
            'description_am': 'Description' + AM_NOTE,
            'event_date': 'Date & Time',
            'image': 'Event Image',
        }


# ── Newsletter / Blog (no Amharic — internal publishing tool) ─────────────────

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'subject', 'content', 'image', 'status', 'scheduled_for']
        widgets = {
            'title': text('Blog Post Title'),
            'subject': text('Short Description (appears under the title)'),
            'content': textarea(
                'Write your blog post content here...\n\nPress Enter twice for new paragraphs.',
                rows=15
            ),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'status': select(),
            'scheduled_for': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
        labels = {
            'title': 'Blog Post Title',
            'subject': 'Short Description',
            'content': 'Article Content',
            'image': 'Blog Post Image (Optional)',
            'status': 'Status',
            'scheduled_for': 'Schedule For (optional)',
        }
        help_texts = {
            'status': 'Set to "Sent" to publish. This will NOT send emails — only controls blog visibility.',
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'title_am', 'summary', 'summary_am', 'content', 'content_am', 'image', 'published']
        widgets = {
            'title': text('Blog Post Title'),
            'title_am': text('የብሎጉ ርዕስ'),
            'summary': text('Brief description shown on the blog page'),
            'summary_am': text('አጭር መግለጫ'),
            'content': textarea('Write your blog post here...', rows=15),
            'content_am': textarea('የብሎጉን ይዘት ይጻፉ...', rows=15),
            'image': file_input(),
            'published': checkbox(),
        }
        labels = {
            'title': 'Title (English)',
            'title_am': 'Title' + AM_NOTE,
            'summary': 'Short Description (English)',
            'summary_am': 'Short Description' + AM_NOTE,
            'content': 'Content (English)',
            'content_am': 'Content' + AM_NOTE,
            'image': 'Image (Optional)',
            'published': 'Publish on blog page',
        }


# ── House Renovation ──────────────────────────────────────────────────────────

class HouseRenovationForm(forms.ModelForm):
    class Meta:
        model = HouseRenovation
        fields = ['name', 'name_am', 'description', 'description_am', 'before_image', 'after_image']
        widgets = {
            'name': text('Beneficiary name'),
            'name_am': text('የተጠቃሚው ስም'),
            'description': textarea('Brief description', rows=3),
            'description_am': textarea('አጭር መግለጫ', rows=3),
            'before_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'after_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        labels = {
            'name': 'Name (English)',
            'name_am': 'Name' + AM_NOTE,
            'description': 'Description (English)',
            'description_am': 'Description' + AM_NOTE,
        }


# ── Story ─────────────────────────────────────────────────────────────────────

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = [
            'name',
            'title', 'title_am',
            'tag', 'tag_am',
            'date_info', 'date_info_am',
            'location_info', 'location_info_am',
            'content', 'content_am',
            'image_1', 'image_1_label', 'image_1_label_am',
            'image_2', 'image_2_label', 'image_2_label_am',
            'image_3', 'image_3_label', 'image_3_label_am',
            'stat_1_number', 'stat_1_text', 'stat_1_text_am',
            'stat_2_number', 'stat_2_text', 'stat_2_text_am',
            'stat_3_number', 'stat_3_text', 'stat_3_text_am',
            'order', 'layout', 'published',
        ]
        widgets = {
            'name': text('e.g., Aboye Waqjira'),
            'title': text('e.g., A Journey from Streets to Dignity'),
            'title_am': text('ለምሳሌ፦ ከጎዳና ወደ ክብር'),
            'tag': text('e.g., Miraculous Recovery'),
            'tag_am': text('ለምሳሌ፦ ተአምራዊ ማገገም'),
            'date_info': text('e.g., Joined May 27, 2018'),
            'date_info_am': text('ለምሳሌ፦ የተቀላቀሉት ግንቦት 27, 2010'),
            'location_info': text('e.g., ROTOM Center'),
            'location_info_am': text('ለምሳሌ፦ ሮቶም ማዕከል'),
            'content': textarea('Write the full story here...', rows=10),
            'content_am': textarea('ሙሉ ታሪኩን ይጻፉ...', rows=10),
            'image_1': file_input(),
            'image_1_label': text('e.g., Before'),
            'image_1_label_am': text('ለምሳሌ፦ ከዚህ በፊት'),
            'image_2': file_input(),
            'image_2_label': text('e.g., After'),
            'image_2_label_am': text('ለምሳሌ፦ ከዚህ በኋላ'),
            'image_3': file_input(),
            'image_3_label': text('e.g., At Center'),
            'image_3_label_am': text('ለምሳሌ፦ በማዕከሉ'),
            'stat_1_number': text('e.g., 6'),
            'stat_1_text': text('e.g., Weeks to Walk'),
            'stat_1_text_am': text('ለምሳሌ፦ ሳምንታት ለመሄድ'),
            'stat_2_number': text('e.g., 100%'),
            'stat_2_text': text('e.g., Independence'),
            'stat_2_text_am': text('ለምሳሌ፦ ነፃነት'),
            'stat_3_number': text('e.g., Miracle'),
            'stat_3_text': text('e.g., Recovery'),
            'stat_3_text_am': text('ለምሳሌ፦ ማገገም'),
            'order': number(),
            'layout': select(),
            'published': checkbox(),
        }
        labels = {
            'name': 'Person\'s Name',
            'title': 'Title (English)',
            'title_am': 'Title' + AM_NOTE,
            'tag': 'Tag (English)',
            'tag_am': 'Tag' + AM_NOTE,
            'date_info': 'Date Info (English)',
            'date_info_am': 'Date Info' + AM_NOTE,
            'location_info': 'Location Info (English)',
            'location_info_am': 'Location Info' + AM_NOTE,
            'content': 'Content (English)',
            'content_am': 'Content' + AM_NOTE,
            'image_1_label': 'Image 1 Label (English)',
            'image_1_label_am': 'Image 1 Label' + AM_NOTE,
            'image_2_label': 'Image 2 Label (English)',
            'image_2_label_am': 'Image 2 Label' + AM_NOTE,
            'image_3_label': 'Image 3 Label (English)',
            'image_3_label_am': 'Image 3 Label' + AM_NOTE,
            'stat_1_text': 'Stat 1 Text (English)',
            'stat_1_text_am': 'Stat 1 Text' + AM_NOTE,
            'stat_2_text': 'Stat 2 Text (English)',
            'stat_2_text_am': 'Stat 2 Text' + AM_NOTE,
            'stat_3_text': 'Stat 3 Text (English)',
            'stat_3_text_am': 'Stat 3 Text' + AM_NOTE,
        }


# ── Donation Package ──────────────────────────────────────────────────────────

class DonationPackageForm(forms.ModelForm):
    class Meta:
        model = DonationPackage
        fields = ['title', 'title_am', 'amount', 'description', 'description_am', 'features', 'features_am', 'order', 'is_active']
        widgets = {
            'title': text('e.g., Home Care Support'),
            'title_am': text('ለምሳሌ፦ የቤት ክብካቤ ድጋፍ'),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1800', 'step': '0.01'}),
            'description': text('e.g., Supports a senior living at home for one month'),
            'description_am': text('ለምሳሌ፦ ለአንድ ወር ቤት ውስጥ ለሚኖር አዛውንት ድጋፍ ይሰጣል'),
            'features': textarea('Enter features, one per line:\nEssential food commodities\nEssential hygiene items', rows=6),
            'features_am': textarea('ባህሪያትን አንድ በአንድ ይጻፉ:\nዋና ዋና የምግብ ዕቃዎች\nዋና ዋና የንፅህና ዕቃዎች', rows=6),
            'order': number(),
            'is_active': checkbox(),
        }
        labels = {
            'title': 'Title (English)',
            'title_am': 'Title' + AM_NOTE,
            'description': 'Description (English)',
            'description_am': 'Description' + AM_NOTE,
            'features': 'Features (English)',
            'features_am': 'Features' + AM_NOTE,
            'order': 'Display Order',
            'is_active': 'Active (Show on Website)',
        }
        help_texts = {
            'features': 'Enter each feature on a new line',
            'features_am': 'Enter each Amharic feature on a new line',
        }


# ── Champion ──────────────────────────────────────────────────────────────────

class ChampionForm(forms.ModelForm):
    class Meta:
        model = Champion
        fields = ['name', 'role', 'role_am', 'quote', 'quote_am', 'image', 'years_supported', 'achievement', 'achievement_am', 'order', 'layout', 'is_active']
        widgets = {
            'name': text('e.g., Meron Tadesse'),
            'role': text('e.g., University Student, Age 19'),
            'role_am': text('ለምሳሌ፦ የዩኒቨርሲቲ ተማሪ፣ ዕድሜ 19'),
            'quote': textarea('Enter their testimonial/story...', rows=8),
            'quote_am': textarea('ምስክርነታቸውን ይጻፉ...', rows=8),
            'image': file_input(),
            'years_supported': text('e.g., 5 or 3-5'),
            'achievement': text('e.g., 1st In Family to University'),
            'achievement_am': text('ለምሳሌ፦ በቤተሰብ ውስጥ ለዩኒቨርሲቲ የደረሰ ቀዳሚ'),
            'order': number(),
            'layout': select(),
            'is_active': checkbox(),
        }
        labels = {
            'role': 'Role (English)',
            'role_am': 'Role' + AM_NOTE,
            'quote': 'Quote / Story (English)',
            'quote_am': 'Quote / Story' + AM_NOTE,
            'achievement': 'Achievement (English)',
            'achievement_am': 'Achievement' + AM_NOTE,
        }


# ── Gallery Image ─────────────────────────────────────────────────────────────

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'title_am', 'caption', 'caption_am', 'image', 'order', 'is_active']
        widgets = {
            'title': text('e.g., Girls Empowerment'),
            'title_am': text('ለምሳሌ፦ የሴቶች ብቃት'),
            'caption': textarea('Enter image description...', rows=3),
            'caption_am': textarea('የምስሉን መግለጫ ይጻፉ...', rows=3),
            'image': file_input(),
            'order': number(),
            'is_active': checkbox(),
        }
        labels = {
            'title': 'Title (English)',
            'title_am': 'Title' + AM_NOTE,
            'caption': 'Caption (English)',
            'caption_am': 'Caption' + AM_NOTE,
        }


# ── Milestone ─────────────────────────────────────────────────────────────────

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['year', 'title', 'title_am', 'description', 'description_am', 'image', 'order', 'position', 'is_active']
        widgets = {
            'year': text('e.g., 2017'),
            'title': text('e.g., Our Beginning'),
            'title_am': text('ለምሳሌ፦ መጀመሪያችን'),
            'description': textarea('Enter milestone description...', rows=4),
            'description_am': textarea('የምዕራፉን መግለጫ ይጻፉ...', rows=4),
            'image': file_input(),
            'order': number(),
            'position': select(),
            'is_active': checkbox(),
        }
        labels = {
            'title': 'Title (English)',
            'title_am': 'Title' + AM_NOTE,
            'description': 'Description (English)',
            'description_am': 'Description' + AM_NOTE,
        }


# ── Team Member ───────────────────────────────────────────────────────────────

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'position', 'position_am', 'image', 'order', 'is_active']
        widgets = {
            'name': text('e.g., Hawi Belete'),
            'position': text('e.g., Director'),
            'position_am': text('ለምሳሌ፦ ዳይሬክተር'),
            'image': file_input(),
            'order': number(),
            'is_active': checkbox(),
        }
        labels = {
            'position': 'Position (English)',
            'position_am': 'Position' + AM_NOTE,
        }


# ── Center Photo ──────────────────────────────────────────────────────────────

class CenterPhotoForm(forms.ModelForm):
    class Meta:
        model = CenterPhoto
        fields = ['title', 'title_am', 'description', 'description_am', 'image', 'order', 'is_active']
        widgets = {
            'title': text('e.g., Dining Room'),
            'title_am': text('ለምሳሌ፦ የምግብ ክፍል'),
            'description': textarea('Brief description...', rows=3),
            'description_am': textarea('አጭር መግለጫ...', rows=3),
            'image': file_input(),
            'order': number(),
            'is_active': checkbox(),
        }
        labels = {
            'title': 'Title (English)',
            'title_am': 'Title' + AM_NOTE,
            'description': 'Description (English)',
            'description_am': 'Description' + AM_NOTE,
        }


# ── Partner ───────────────────────────────────────────────────────────────────

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'logo', 'website', 'description', 'description_am', 'order', 'is_active']
        widgets = {
            'name': text('e.g. Beautiful World Canada'),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'description': textarea('Brief description of the partnership...', rows=3),
            'description_am': textarea('አጭር የሽርክና መግለጫ...', rows=3),
            'order': number('10, 20, 30...'),
            'is_active': checkbox(),
        }
        labels = {
            'name': 'Organization Name',
            'logo': 'Partner Logo',
            'website': 'Website URL (optional)',
            'description': 'Description (English, optional)',
            'description_am': 'Description' + AM_NOTE,
            'order': 'Display Order',
            'is_active': 'Active (Show on Website)',
        }
        help_texts = {
            'logo': 'Recommended: PNG with transparent background, 200x200px to 400x400px',
            'order': 'Lower numbers appear first. Use increments of 10 for easy reordering',
        }


# ── Testimonial ───────────────────────────────────────────────────────────────

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'role_am', 'quote', 'quote_am', 'image', 'order', 'is_active']
        widgets = {
            'name': text('e.g., Senior Tsige'),
            'role': text('e.g., Program Beneficiary'),
            'role_am': text('ለምሳሌ፦ የፕሮግራም ተጠቃሚ'),
            'quote': textarea('Enter their testimonial...', rows=6),
            'quote_am': textarea('ምስክርነታቸውን ይጻፉ...', rows=6),
            'image': file_input(),
            'order': number(),
            'is_active': checkbox(),
        }
        labels = {
            'name': 'Name',
            'role': 'Role / Title (English)',
            'role_am': 'Role / Title' + AM_NOTE,
            'quote': 'Testimonial (English)',
            'quote_am': 'Testimonial' + AM_NOTE,
            'image': 'Photo (Optional)',
            'order': 'Display Order',
            'is_active': 'Active (Show on Website)',
        }
        help_texts = {
            'image': 'Optional photo (will be auto-compressed to 800x800)',
            'order': 'Lower numbers appear first (0, 1, 2...)',
        }
