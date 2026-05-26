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
    path('delete-event/<int:pk>/', views.delete_event, name='delete_event'),
    path('delete-previous-event/<int:pk>/', views.delete_previous_event, name='delete_previous_event'),
    path('manage-contacts/', views.manage_contacts, name='manage_contacts'),
    path('manage-payments/', views.manage_payments, name='manage_payments'),
    path('manage-registrations/', views.manage_registrations, name='manage_registrations'),
    # Blog Post URLs
    path('manage-blog/', views.manage_blog, name='manage_blog'),
    path('create-blog/', views.create_blog, name='create_blog'),
    path('edit-blog/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('delete-blog/<int:pk>/', views.delete_blog, name='delete_blog'),
    # Email Subscribers
    path('send-email/', views.send_email_to_subscribers, name='send_email'),
    path('manage-subscribers/', views.manage_subscribers, name='manage_subscribers'),
    path('export-subscribers/', views.export_subscribers, name='export_subscribers'),
    # House Renovations
    path('manage-renovations/', views.manage_renovations, name='manage_renovations'),
    path('create-renovation/', views.create_renovation, name='create_renovation'),
    path('edit-renovation/<int:pk>/', views.edit_renovation, name='edit_renovation'),
    path('delete-renovation/<int:pk>/', views.delete_renovation, name='delete_renovation'),
    # Stories
    path('manage-stories/', views.manage_stories, name='manage_stories'),
    path('create-story/', views.create_story, name='create_story'),
    path('edit-story/<int:pk>/', views.edit_story, name='edit_story'),
    path('delete-story/<int:pk>/', views.delete_story, name='delete_story'),
    # Donation Packages
    path('manage-packages/', views.manage_packages, name='manage_packages'),
    path('create-package/', views.create_package, name='create_package'),
    path('edit-package/<int:pk>/', views.edit_package, name='edit_package'),
    path('delete-package/<int:pk>/', views.delete_package, name='delete_package'),
    # Champions
    path('manage-champions/', views.manage_champions, name='manage_champions'),
    path('create-champion/', views.create_champion, name='create_champion'),
    path('edit-champion/<int:pk>/', views.edit_champion, name='edit_champion'),
    path('delete-champion/<int:pk>/', views.delete_champion, name='delete_champion'),
    # Gallery
    path('manage-gallery/', views.manage_gallery, name='manage_gallery'),
    path('create-gallery-image/', views.create_gallery_image, name='create_gallery_image'),
    path('edit-gallery-image/<int:pk>/', views.edit_gallery_image, name='edit_gallery_image'),
    path('delete-gallery-image/<int:pk>/', views.delete_gallery_image, name='delete_gallery_image'),
    # Milestones
    path('manage-milestones/', views.manage_milestones, name='manage_milestones'),
    path('create-milestone/', views.create_milestone, name='create_milestone'),
    path('edit-milestone/<int:pk>/', views.edit_milestone, name='edit_milestone'),
    path('delete-milestone/<int:pk>/', views.delete_milestone, name='delete_milestone'),
    # Team Members
    path('manage-team/', views.manage_team, name='manage_team'),
    path('create-team-member/', views.create_team_member, name='create_team_member'),
    path('edit-team-member/<int:pk>/', views.edit_team_member, name='edit_team_member'),
    path('delete-team-member/<int:pk>/', views.delete_team_member, name='delete_team_member'),
    # Center Photos
    path('manage-center-photos/', views.manage_center_photos, name='manage_center_photos'),
    path('create-center-photo/', views.create_center_photo, name='create_center_photo'),
    path('edit-center-photo/<int:pk>/', views.edit_center_photo, name='edit_center_photo'),
    path('delete-center-photo/<int:pk>/', views.delete_center_photo, name='delete_center_photo'),
    # Partners
    path('manage-partners/', views.manage_partners, name='manage_partners'),
    path('create-partner/', views.create_partner, name='create_partner'),
    path('edit-partner/<int:pk>/', views.edit_partner, name='edit_partner'),
    path('delete-partner/<int:pk>/', views.delete_partner, name='delete_partner'),
    # Testimonials
    path('manage-testimonials/', views.manage_testimonials, name='manage_testimonials'),
    path('create-testimonial/', views.create_testimonial, name='create_testimonial'),
    path('edit-testimonial/<int:pk>/', views.edit_testimonial, name='edit_testimonial'),
    path('delete-testimonial/<int:pk>/', views.delete_testimonial, name='delete_testimonial'),
    # Newsletter URLs
    path('manage-newsletters/', views.manage_newsletters, name='manage_newsletters'),
    path('create-newsletter/', views.create_newsletter, name='create_newsletter'),
    path('edit-newsletter/<int:pk>/', views.edit_newsletter, name='edit_newsletter'),
    path('newsletter/<int:pk>/', views.newsletter_detail, name='newsletter_detail'),
    path('newsletter/<int:pk>/preview/', views.preview_newsletter, name='preview_newsletter'),
    # Volunteer Gallery
    path('manage-volunteer-gallery/', views.manage_volunteer_gallery, name='manage_volunteer_gallery'),
    path('create-volunteer-gallery-image/', views.create_volunteer_gallery_image, name='create_volunteer_gallery_image'),
    path('edit-volunteer-gallery-image/<int:pk>/', views.edit_volunteer_gallery_image, name='edit_volunteer_gallery_image'),
    path('delete-volunteer-gallery-image/<int:pk>/', views.delete_volunteer_gallery_image, name='delete_volunteer_gallery_image'),
    # Detail views
    path('volunteer/<int:pk>/', views.volunteer_detail, name='volunteer_detail'),
    path('delete-volunteer/<int:pk>/', views.delete_volunteer, name='delete_volunteer'),
    path('contact/<int:pk>/', views.contact_detail, name='contact_detail'),
    path('payment/<int:pk>/', views.payment_detail, name='payment_detail'),
    path('registration/<int:pk>/', views.registration_detail, name='registration_detail'),
    # Site Content (Static Text Editor)
    path('site-content/', views.manage_site_content, name='manage_site_content'),
    path('site-content/<str:page_slug>/', views.edit_page_content, name='edit_page_content'),
]