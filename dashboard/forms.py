# dashboard/forms.py (add this to the existing forms.py)
from django import forms
from rotom.models import Event, PreviousEvent, Newsletter, BlogPost, Story, DonationPackage, Champion, GalleryImage, Milestone, TeamMember, CenterPhoto, Partner, Testimonial

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Event Description'}),
            'event_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'event_date': 'Date & Time',
            'image': 'Event Image',
        }

class PreviousEventForm(forms.ModelForm):
    class Meta:
        model = PreviousEvent
        fields = ['title', 'description', 'event_date', 'image']  # Added 'description' to fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Event Description'}),  # Added widget for description
            'event_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',  # Added label for description
            'event_date': 'Date & Time',
            'image': 'Event Image',
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'subject', 'content', 'image', 'status', 'scheduled_for']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Blog Post Title'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Short Description (appears under the title)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 15, 
                'placeholder': 'Write your blog post content here...\n\nYou can write multiple paragraphs naturally.\n\nJust press Enter twice to create new paragraphs.\n\nNo HTML tags needed!'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'scheduled_for': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
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
            'title': 'This will be the main headline of your blog post',
            'subject': 'Brief summary that appears under the title (like a subtitle)',
            'content': 'Write your blog post content here. No HTML tags needed - just write naturally with paragraphs.',
            'image': 'Upload an image for your blog post. Keep file size reasonable (under 2MB recommended).',
            'status': 'Set to "Sent" to publish on blog page, "Draft" to keep private. This will NOT send emails - only controls blog visibility.',
            'scheduled_for': 'Leave empty for immediate publishing when status is changed to "Sent"',
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'summary', 'content', 'image', 'published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Post Title'}),
            'summary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief description shown on the blog page'}),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 15,
                'placeholder': 'Write your blog post here...\n\nPress Enter twice to create new paragraphs.\n\nNo HTML tags needed!'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Title',
            'summary': 'Short Description',
            'content': 'Content',
            'image': 'Image (Optional)',
            'published': 'Publish on blog page',
        }


from rotom.models import HouseRenovation

class HouseRenovationForm(forms.ModelForm):
    class Meta:
        model = HouseRenovation
        fields = ['name', 'description', 'before_image', 'after_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Beneficiary name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description'}),
            'before_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'after_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = [
            'name', 'title', 'tag', 'date_info', 'location_info', 'content',
            'image_1', 'image_1_label', 'image_2', 'image_2_label', 'image_3', 'image_3_label',
            'stat_1_number', 'stat_1_text', 'stat_2_number', 'stat_2_text', 'stat_3_number', 'stat_3_text',
            'order', 'layout', 'published'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Aboye Waqjira'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., A Journey from Streets to Dignity'}),
            'tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Miraculous Recovery'}),
            'date_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Joined May 27, 2018'}),
            'location_info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., ROTOM Center'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Write the full story here. Use double line breaks for paragraphs.'}),
            'image_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'image_1_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Before'}),
            'image_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'image_2_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., After'}),
            'image_3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'image_3_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., At Center'}),
            'stat_1_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 6'}),
            'stat_1_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Weeks to Walk'}),
            'stat_2_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 100%'}),
            'stat_2_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Independence'}),
            'stat_3_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Miracle'}),
            'stat_3_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Recovery'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'layout': forms.Select(attrs={'class': 'form-control'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class DonationPackageForm(forms.ModelForm):
    class Meta:
        model = DonationPackage
        fields = ['title', 'amount', 'description', 'features', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Home Care Support'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1800', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Supports a senior living at home for one month'}),
            'features': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Enter features, one per line:\nEssential food commodities\nEssential hygiene items\nSocial outings and lunches'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'features': 'Enter each feature on a new line',
        }



class ChampionForm(forms.ModelForm):
    class Meta:
        model = Champion
        fields = ['name', 'role', 'quote', 'image', 'years_supported', 'achievement', 'order', 'layout', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Meron Tadesse'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., University Student, Age 19'}),
            'quote': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Enter their testimonial/story...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'years_supported': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5 or 3-5'}),
            'achievement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1st In Family to University'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'layout': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'caption', 'image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Girls Empowerment'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter image description...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        fields = ['year', 'title', 'description', 'image', 'order', 'position', 'is_active']
        widgets = {
            'year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2017'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Our Beginning'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter milestone description...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'position', 'image', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Hawi Belete'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Director'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CenterPhotoForm(forms.ModelForm):
    class Meta:
        model = CenterPhoto
        fields = ['title', 'description', 'image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Dining Room'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'logo', 'website', 'description', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Beautiful World Canada'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of the partnership...'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '10, 20, 30...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Organization Name',
            'logo': 'Partner Logo',
            'website': 'Website URL (optional)',
            'description': 'Description (optional)',
            'order': 'Display Order',
            'is_active': 'Active (Show on Website)',
        }
        help_texts = {
            'name': 'Full name of the partner organization',
            'logo': 'Recommended: PNG with transparent background, 200x200px to 400x400px',
            'website': 'Optional link to their website',
            'description': 'Brief description of the partnership (optional)',
            'order': 'Lower numbers appear first. Use increments of 10 (10, 20, 30) for easy reordering',
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'quote', 'image', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Sarah Johnson'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Volunteer, Donor, Partner'}),
            'quote': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Enter their testimonial/feedback...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Name',
            'role': 'Role/Title',
            'quote': 'Testimonial',
            'image': 'Photo (Optional)',
            'order': 'Display Order',
            'is_active': 'Active (Show on Website)',
        }
        help_texts = {
            'name': 'Full name of the person giving the testimonial',
            'role': 'Their relationship to ROTOM (e.g., Volunteer, Donor, Beneficiary, Partner)',
            'quote': 'Their testimonial or feedback about ROTOM',
            'image': 'Optional photo (will be auto-compressed to 800x800)',
            'order': 'Lower numbers appear first (0, 1, 2...)',
        }
