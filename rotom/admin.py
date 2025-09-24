# from django.contrib import admin
# from .models import Contact, Event, PreviousEvent,  Payment, VolunteerProfile, Day, InterestCategory

# # Register models without custom admin classes
# admin.site.register(VolunteerProfile)
# admin.site.register(Day)
# admin.site.register(InterestCategory)
# admin.site.register(Contact)

# # Admin class for Event
# @admin.register(Event)
# class EventAdmin(admin.ModelAdmin):
#     list_display = ('title', 'event_date')
#     ordering = ['-event_date']

# # Admin class for previousEvent
# @admin.register(PreviousEvent)
# class PreviousEventAdmin(admin.ModelAdmin):
#     list_display = ('title', 'event_date')  # Assuming previousEvent has similar fields
#     ordering = ['-event_date']

# # Admin class for Payment
# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('tx_ref', 'amount', 'status', 'email', 'first_name', 'last_name', 'created_at')
#     ordering = ['-created_at']
#     list_filter = ('status',)
#     search_fields = ('tx_ref', 'email', 'first_name', 'last_name')

#     def get_queryset(self, request):
#         """Show only payments with status='success' in the admin interface."""
#         qs = super().get_queryset(request)
#         return qs.filter(status='success')