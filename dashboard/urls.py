# urls.py (add edit URLs to your dashboard app's urls.py)
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-volunteers/', views.manage_volunteers, name='manage_volunteers'),
    path('manage-events/', views.manage_events, name='manage_events'),
    path('create-event/', views.create_event, name='create_event'),
    path('edit-event/<int:pk>/', views.edit_event, name='edit_event'),
    path('create-previous-event/', views.create_previous_event, name='create_previous_event'),
    path('edit-previous-event/<int:pk>/', views.edit_previous_event, name='edit_previous_event'),
    path('manage-contacts/', views.manage_contacts, name='manage_contacts'),
    path('manage-payments/', views.manage_payments, name='manage_payments'),
    path('manage-registrations/', views.manage_registrations, name='manage_registrations'),
    # Detail views
    path('volunteer/<int:pk>/', views.volunteer_detail, name='volunteer_detail'),
    path('contact/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('payment/<int:pk>/', views.payment_detail, name='payment_detail'),
    
    path('registration/<int:pk>/', views.registration_detail, name='registration_detail'),
]