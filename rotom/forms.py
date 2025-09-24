from pyexpat.errors import messages
from django import forms
from django.shortcuts import redirect, render
from .models import Contact, FeedingRegistration, Subscriber, VolunteerProfile, Day

class VolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = VolunteerProfile
        fields = ['first_name', 'last_name', 'age', 'phone_number', 'education_level', 'days_available', 'times_available', 'interests']
        widgets = {
            'days_available': forms.CheckboxSelectMultiple(),  # Allow multiple selections
            'times_available': forms.RadioSelect(),
            'interests': forms.CheckboxSelectMultiple(),
            'education_level': forms.Select(),
        }
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.startswith("+"):
            raise forms.ValidationError("Phone number must include a country code and start with '+'")
        return phone_number




class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'location', 'email', 'phone_number', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'placeholder': 'Your Location', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number (optional)', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control', 'rows': 5}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or '@' not in email or '.' not in email:
            raise forms.ValidationError("Please enter a valid email address.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and (not phone.startswith(('09', '07')) or len(phone) != 10 or not phone.isdigit()):
            raise forms.ValidationError("Phone number must be 10 digits starting with 09 or 07.")
        return phone
    


class FeedingRegistrationForm(forms.ModelForm):
    class Meta:
        model = FeedingRegistration
        fields = ['full_name', 'email', 'phone', 'meal_type', 'location', 'preferred_date', 'notes']
        labels = {
            'full_name': 'Full Name / ሙሉ ስም',
            'email': 'Email Address / የኢሜይል አድራሻ',
            'phone': 'Phone Number / ስልክ ቁጥር',
            'meal_type': 'Meal Type / የምግብ አይነት',
            'location': 'Location / ቦታ',
            'preferred_date': 'Preferred Date / ተመራጭ ቀን',
            'notes': 'Additional Notes / ተጨማሪ ማስታወሻዎች',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name / ሙሉ ስምዎን ያስገቡ', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email / ኢሜይልዎን ያስገቡ', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number / ስልክ ቁጥርዎን ያስገቡ', 'class': 'form-control'}),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'placeholder': 'E.g., type of food, number of meals, or special requests / ለምሳሌ፣ የምግብ አይነት፣ የምግቦች ብዛት፣ ወይም ልዩ ጥያቄዎች', 'rows': 4, 'class': 'form-control'}),
        }

class SubscriberForm(forms.ModelForm):
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email Address',
            'class': 'newsletter-input'
        })
    )

    class Meta:
        model = Subscriber
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already subscribed.')
        return email