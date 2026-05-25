from django.contrib import admin
from django.db import models
from .models import (
    VolunteerProfile, Day, InterestCategory, Contact, 
    Event, PreviousEvent, Payment, FeedingRegistration, Subscriber, Newsletter, HouseRenovation, Story, DonationPackage, Champion, GalleryImage, Milestone, TeamMember, CenterPhoto, NavbarPattern, Partner, Testimonial, VolunteerGallery
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
    list_display = ('full_name', 'gender', 'age', 'address', 'phone_number', 'education_level', 'days_list', 'created_at')
    list_filter = ('gender', 'address', 'education_level', 'times_available', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone_number')
    readonly_fields = ('created_at',)
    filter_horizontal = ('days_available', 'interests')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'gender', 'age', 'phone_number', 'address', 'education_level')
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
    
    def days_list(self, obj):
        days = obj.days_available.all()
        if days:
            return ", ".join([day.name for day in days])
        return "Not specified"
    days_list.short_description = 'Days Available'

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
    
    # Show only successful payments by default
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If no status filter is applied, show only successful payments
        if not request.GET.get('status'):
            return qs.filter(status='success')
        return qs
    
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
    actions = ['export_emails']

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_subscribers'] = Subscriber.objects.count()
        return super().changelist_view(request, extra_context=extra_context)

    def export_emails(self, request, queryset):
        from django.http import HttpResponse
        emails = '\n'.join(queryset.values_list('email', flat=True))
        response = HttpResponse(emails, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="subscribers.txt"'
        return response
    export_emails.short_description = 'Export selected emails as .txt'

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

@admin.register(HouseRenovation)
class HouseRenovationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'tag', 'order', 'layout', 'published', 'created_at')
    list_filter = ('published', 'layout', 'created_at')
    search_fields = ('name', 'title', 'tag', 'content')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'published')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'tag', 'date_info', 'location_info')
        }),
        ('Story Content', {
            'fields': ('content',)
        }),
        ('Images', {
            'fields': (
                ('image_1', 'image_1_label'),
                ('image_2', 'image_2_label'),
                ('image_3', 'image_3_label')
            )
        }),
        ('Statistics', {
            'fields': (
                ('stat_1_number', 'stat_1_text'),
                ('stat_2_number', 'stat_2_text'),
                ('stat_3_number', 'stat_3_text')
            )
        }),
        ('Display Settings', {
            'fields': ('order', 'layout', 'published')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(DonationPackage)
class DonationPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'features')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Package Information', {
            'fields': ('title', 'amount', 'description')
        }),
        ('Features', {
            'fields': ('features',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Champion)
class ChampionAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'years_supported', 'order', 'layout', 'is_active', 'created_at')
    list_filter = ('is_active', 'layout', 'created_at')
    search_fields = ('name', 'role', 'quote')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Champion Information', {
            'fields': ('name', 'role', 'quote', 'image')
        }),
        ('Impact', {
            'fields': ('years_supported', 'achievement')
        }),
        ('Display Settings', {
            'fields': ('order', 'layout', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'caption')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'caption', 'image')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'position', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'position', 'created_at')
    search_fields = ('year', 'title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Milestone Information', {
            'fields': ('year', 'title', 'description', 'image')
        }),
        ('Display Settings', {
            'fields': ('order', 'position', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'position')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Team Member Information', {
            'fields': ('name', 'position', 'image')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CenterPhoto)
class CenterPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Photo Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(NavbarPattern)
class NavbarPatternAdmin(admin.ModelAdmin):
    list_display = ('name', 'height', 'opacity', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active',)
    fieldsets = (
        ('Pattern Information', {
            'fields': ('name', 'image'),
            'description': 'Upload a horizontal repeating pattern image. PNG or JPG format recommended.'
        }),
        ('Display Settings', {
            'fields': ('height', 'opacity', 'is_active'),
            'description': 'Adjust the pattern bar height and opacity. Only one pattern can be active at a time.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_active:
            from django.contrib import messages
            messages.success(request, f'Pattern "{obj.name}" is now active on the navbar!')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'has_website', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Partner Information', {
            'fields': ('name', 'logo', 'website', 'description'),
            'description': 'Add partner organization details. Logo should be a transparent PNG for best results.'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active'),
            'description': 'Control the display order and visibility of this partner.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def has_website(self, obj):
        return bool(obj.website)
    has_website.boolean = True
    has_website.short_description = 'Website'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'role', 'quote')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Testimonial Information', {
            'fields': ('name', 'role', 'quote', 'image'),
            'description': 'Add testimonials from volunteers, donors, partners, or beneficiaries.'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active'),
            'description': 'Control the display order and visibility of this testimonial.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(VolunteerGallery)
class VolunteerGalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at',)
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Image Information', {
            'fields': ('title', 'image'),
            'description': 'Upload a photo for the volunteer gallery.'
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active'),
            'description': 'Control the display order and visibility in the gallery.'
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )


# Optional: Custom admin site header
admin.site.site_header = 'REACH ONE ETH Administration'
admin.site.site_title = 'REACH ONE ETH Admin'
admin.site.index_title = 'Welcome to REACH ONE ETH Admin Panel'