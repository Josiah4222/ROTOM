# dashboard/forms.py (add this to the existing forms.py)
from django import forms
from rotom.models import Event, PreviousEvent  # Import from rotom app

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