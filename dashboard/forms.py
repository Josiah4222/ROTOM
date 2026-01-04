# dashboard/forms.py (add this to the existing forms.py)
from django import forms
from rotom.models import Event, PreviousEvent, Newsletter  # Import from rotom app

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