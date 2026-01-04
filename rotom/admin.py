from django.contrib import admin
from django.db import models
from .models import (
    VolunteerProfile, Day, InterestCategory, Contact, 
    Event, PreviousEvent, Payment, FeedingRegistration, Subscriber, Newsletter
)

# Inline for VolunteerProfile
class InterestCategoryInline(admin.TabularInline):
    model = VolunteerProfile.interests.through
    extra = 1

class DayInline(admin.TabularInline):
    model = VolunteerProfile.days_available.through
    extra = 1

# Admin class for VolunteerProfile
@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'age', 'phone_number', 'education_level', 'created_at')
    list_filter = ('education_level', 'times_available', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')
    readonly_fields = ('created_at',)
    filter_horizontal = ('days_available', 'interests')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'age', 'phone_number', 'education_level')
        }),
        ('Availability', {
            'fields': ('days_available', 'times_available')
        }),
        ('Interests', {
            'fields': ('interests',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

# Admin class for Day
@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('name', 'volunteer_count')
    search_fields = ('name',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(volunteer_count_annotated=models.Count('volunteerprofile'))
    
    def volunteer_count(self, obj):
        return obj.volunteer_count_annotated
    volunteer_count.short_description = 'Volunteers'

# Admin class for InterestCategory
@admin.register(InterestCategory)
class InterestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'volunteer_count')
    search_fields = ('name',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(volunteer_count_annotated=models.Count('volunteerprofile'))
    
    def volunteer_count(self, obj):
        return obj.volunteer_count_annotated
    volunteer_count.short_description = 'Volunteers'

# Admin class for Contact
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'location', 'phone_number', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('name', 'email', 'phone_number', 'message')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone_number', 'location')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

# Admin class for Event
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'created_at')
    list_filter = ('event_date', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'event_date', 'image')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

# Admin class for PreviousEvent
@admin.register(PreviousEvent)
class PreviousEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'created_at')
    list_filter = ('event_date', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'event_date', 'image')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

# Admin class for Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tx_ref', 'full_name', 'email', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('tx_ref', 'email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at', 'tx_ref')
    fieldsets = (
        ('Payment Information', {
            'fields': ('tx_ref', 'amount', 'status')
        }),
        ('Donor Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Donor Name'

# Admin class for FeedingRegistration
@admin.register(FeedingRegistration)
class FeedingRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'meal_type', 'location', 'preferred_date', 'created_at')
    list_filter = ('meal_type', 'location', 'preferred_date', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'notes')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Meal Details', {
            'fields': ('meal_type', 'location', 'preferred_date')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

# Admin class for Subscriber
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    list_filter = ('subscribed_at',)
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)
    fieldsets = (
        ('Subscriber Information', {
            'fields': ('email',)
        }),
        ('Metadata', {
            'fields': ('subscribed_at',),
            'classes': ('collapse',)
        })
    )

# Admin class for Newsletter
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'status', 'recipients_count', 'created_at', 'sent_at')
    list_filter = ('status', 'created_at', 'sent_at')
    search_fields = ('title', 'subject', 'content')
    readonly_fields = ('created_at', 'sent_at', 'recipients_count')
    fieldsets = (
        ('Blog Post Details', {
            'fields': ('title', 'subject', 'content', 'image'),
            'description': 'Create your blog post content here. The title will appear as the blog post headline, and content will be the article body.'
        }),
        ('Publishing', {
            'fields': ('status',),
            'description': 'Set status to "Sent" to publish on blog page. Draft posts won\'t appear publicly. Note: This will NOT send emails - it only controls blog visibility.'
        }),
        ('Email Settings (Optional)', {
            'fields': ('scheduled_for',),
            'classes': ('collapse',),
            'description': 'Only use if you want to actually send newsletters via email'
        }),
        ('Metadata', {
            'fields': ('created_at', 'sent_at', 'recipients_count'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        # Don't trigger email sending - just save the model
        # This allows us to use "Sent" status for blog publishing without sending emails
        obj.save()
        
        # If user specifically wants to send emails, they can do it manually
        # For now, we just use status for blog visibility
        if obj.status == 'sent' and not obj.sent_at:
            # Mark as sent for blog purposes but don't actually send emails
            from django.utils import timezone
            obj.sent_at = timezone.now()
            obj.save()
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Update help text and labels for blog context
        if 'title' in form.base_fields:
            form.base_fields['title'].label = 'Blog Post Title'
            form.base_fields['title'].help_text = 'This will be the main headline of your blog post'
        if 'subject' in form.base_fields:
            form.base_fields['subject'].label = 'Short Description'
            form.base_fields['subject'].help_text = 'Brief summary that appears under the title (like a subtitle)'
        if 'content' in form.base_fields:
            form.base_fields['content'].label = 'Article Content'
            form.base_fields['content'].help_text = 'Write your blog post content here. No HTML tags needed - just write naturally with paragraphs.'
            form.base_fields['content'].widget.attrs.update({
                'rows': 20,
                'placeholder': 'Write your blog post content here...\n\nYou can write multiple paragraphs naturally.\n\nJust press Enter twice to create new paragraphs.\n\nNo HTML tags needed!'
            })
        if 'image' in form.base_fields:
            form.base_fields['image'].label = 'Blog Post Image (Optional)'
            form.base_fields['image'].help_text = 'Upload an image for your blog post. Keep file size reasonable (under 2MB recommended).'
        if 'status' in form.base_fields:
            form.base_fields['status'].help_text = 'Set to "Sent" to publish on blog page, "Draft" to keep private. This will NOT send emails - only controls blog visibility.'
        return form

# Optional: Custom admin site header
admin.site.site_header = 'REACH ONE ETH Administration'
admin.site.site_title = 'REACH ONE ETH Admin'
admin.site.index_title = 'Welcome to REACH ONE ETH Admin Panel'