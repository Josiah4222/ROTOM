from django.contrib import admin
from .models import (
    VolunteerProfile, Day, InterestCategory, Contact, 
    Event, PreviousEvent, Payment, FeedingRegistration, Subscriber
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
    
    def volunteer_count(self, obj):
        return obj.volunteerprofile_set.count()
    volunteer_count.short_description = 'Volunteers'

# Admin class for InterestCategory
@admin.register(InterestCategory)
class InterestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'volunteer_count')
    search_fields = ('name',)
    
    def volunteer_count(self, obj):
        return obj.volunteerprofile_set.count()
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

# Optional: Custom admin site header
admin.site.site_header = 'REACH ONE ETH Administration'
admin.site.site_title = 'REACH ONE ETH Admin'
admin.site.index_title = 'Welcome to REACH ONE ETH Admin Panel'