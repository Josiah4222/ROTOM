# views.py (add edit views for Event and PreviousEvent)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.conf import settings
from django.db import models

from rotom.models import Contact, Event, FeedingRegistration, Payment, PreviousEvent, VolunteerProfile, Newsletter, Subscriber, BlogPost, HouseRenovation, Story, DonationPackage, Champion, GalleryImage, Testimonial, VolunteerGallery
from .forms import EventForm, PreviousEventForm, NewsletterForm  # Import the new form

def custom_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard:admin_dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                return redirect('dashboard:admin_dashboard')
            else:
                messages.error(request, "You don't have permission to access the admin panel.")
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'dashboard/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')  # Adjust to your main home URL if needed

@staff_member_required(login_url='dashboard:login')
def admin_dashboard(request):
    from django.db.models import Count, Q
    now = timezone.now()
    
    # Use aggregation instead of separate queries
    stats = {
        'total_volunteers': VolunteerProfile.objects.count(),
        'total_events': Event.objects.filter(event_date__gte=now).count(),
        'total_previous_events': PreviousEvent.objects.count(),
        'total_payments': Payment.objects.filter(status='success').count(),
        'total_contacts': Contact.objects.count(),
        'total_registrations': FeedingRegistration.objects.count(),
        'total_newsletters': Newsletter.objects.count(),
        'total_subscribers': Subscriber.objects.count(),
        'total_volunteer_photos': VolunteerGallery.objects.count(),
    }

    # Use select_related for foreign keys in recent queries
    recent_volunteers = VolunteerProfile.objects.select_related().order_by('-id')[:5]
    recent_contacts = Contact.objects.select_related().order_by('-created_at')[:5]
    recent_payments = Payment.objects.filter(status='success').select_related().order_by('-created_at')[:5]
    recent_registrations = FeedingRegistration.objects.select_related().order_by('-created_at')[:5]
    recent_newsletters = Newsletter.objects.select_related().order_by('-created_at')[:5]

    context = {
        **stats,
        'recent_volunteers': recent_volunteers,
        'recent_contacts': recent_contacts,
        'recent_payments': recent_payments,
        'recent_registrations': recent_registrations,
        'recent_newsletters': recent_newsletters,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@staff_member_required(login_url='dashboard:login')
def manage_volunteers(request):
    search = request.GET.get('search', '')
    volunteers = VolunteerProfile.objects.all().order_by('-id')
    if search:
        volunteers = volunteers.filter(
            models.Q(first_name__icontains=search) |
            models.Q(last_name__icontains=search) |
            models.Q(phone_number__icontains=search)
        )
    paginator = Paginator(volunteers, 10)
    volunteers_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_volunteers.html', {
        'volunteers': volunteers_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
@staff_member_required(login_url='dashboard:login')
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_at = timezone.now()
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('dashboard:manage_events')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventForm()
    return render(request, 'dashboard/create_event.html', {'form': form})

@staff_member_required(login_url='dashboard:login')
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('dashboard:manage_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'dashboard/edit_event.html', {'form': form, 'event': event})

@staff_member_required(login_url='dashboard:login')
def create_previous_event(request):
    if request.method == 'POST':
        form = PreviousEventForm(request.POST, request.FILES)
        if form.is_valid():
            previous_event = form.save(commit=False)
            previous_event.created_at = timezone.now()
            previous_event.save()
            messages.success(request, 'Previous event added successfully!')
            return redirect('dashboard:manage_events')
    else:
        form = PreviousEventForm()
    return render(request, 'dashboard/create_previous_event.html', {'form': form})

@staff_member_required(login_url='dashboard:login')
def edit_previous_event(request, pk):
    previous_event = get_object_or_404(PreviousEvent, pk=pk)
    if request.method == 'POST':
        form = PreviousEventForm(request.POST, request.FILES, instance=previous_event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Previous event updated successfully!')
            return redirect('dashboard:manage_events')
    else:
        form = PreviousEventForm(instance=previous_event)
    return render(request, 'dashboard/edit_previous_event.html', {'form': form, 'previous_event': previous_event})

@staff_member_required(login_url='dashboard:login')
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('dashboard:manage_events')

@staff_member_required(login_url='dashboard:login')
def delete_previous_event(request, pk):
    previous_event = get_object_or_404(PreviousEvent, pk=pk)
    previous_event.delete()
    messages.success(request, 'Previous event deleted successfully!')
    return redirect('dashboard:manage_events')

@staff_member_required(login_url='dashboard:login')
def manage_events(request):
    from django.http import JsonResponse
    from django.template.loader import render_to_string
    now = timezone.now()
    search = request.GET.get('search', '')

    upcoming_qs = Event.objects.filter(event_date__gte=now).order_by('event_date')
    past_qs = PreviousEvent.objects.all().order_by('-event_date')

    if search:
        upcoming_qs = upcoming_qs.filter(title__icontains=search)
        past_qs = past_qs.filter(title__icontains=search)

    paginator_upcoming = Paginator(upcoming_qs, 5)
    paginator_past = Paginator(past_qs, 5)

    upcoming_paginated = paginator_upcoming.get_page(request.GET.get('upcoming_page'))
    past_paginated = paginator_past.get_page(request.GET.get('past_page'))

    context = {
        'upcoming_events': upcoming_paginated,
        'past_events': past_paginated,
        'search': search,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'upcoming_html': render_to_string('dashboard/partials/upcoming_events_table.html', context, request=request),
            'past_html': render_to_string('dashboard/partials/past_events_table.html', context, request=request),
        })

    return render(request, 'dashboard/manage_events.html', context)

@staff_member_required(login_url='dashboard:login')
def manage_contacts(request):
    search = request.GET.get('search', '')
    contacts = Contact.objects.all().order_by('-created_at')
    if search:
        contacts = contacts.filter(
            models.Q(name__icontains=search) |
            models.Q(email__icontains=search) |
            models.Q(message__icontains=search)
        )
    paginator = Paginator(contacts, 10)
    contacts_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_contacts.html', {
        'contacts': contacts_paginated,
        'search': search,
    })

# dashboard/views.py (updated manage_payments to show all for debugging)
@staff_member_required(login_url='dashboard:login')
def manage_payments(request):
    search = request.GET.get('search', '')
    # Only show successful payments
    payments = Payment.objects.filter(status='success').order_by('-created_at')
    if search:
        payments = payments.filter(
            models.Q(first_name__icontains=search) |
            models.Q(last_name__icontains=search) |
            models.Q(email__icontains=search) |
            models.Q(tx_ref__icontains=search)
        )
    paginator = Paginator(payments, 10)
    payments_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_payments.html', {
        'payments': payments_paginated,
        'search': search,
    })
@staff_member_required(login_url='dashboard:login')
def manage_registrations(request):
    search = request.GET.get('search', '')
    registrations = FeedingRegistration.objects.all().order_by('-created_at')
    if search:
        registrations = registrations.filter(
            models.Q(full_name__icontains=search) |
            models.Q(email__icontains=search) |
            models.Q(phone__icontains=search)
        )
    paginator = Paginator(registrations, 10)
    registrations_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_registrations.html', {
        'registrations': registrations_paginated,
        'search': search,
    })

# Placeholder detail views (expand as needed)
@staff_member_required(login_url='dashboard:login')
def volunteer_detail(request, pk):
    volunteer = get_object_or_404(VolunteerProfile, pk=pk)
    return render(request, 'dashboard/volunteer_detail.html', {'volunteer': volunteer})

@staff_member_required(login_url='dashboard:login')
def delete_volunteer(request, pk):
    volunteer = get_object_or_404(VolunteerProfile, pk=pk)
    volunteer.delete()
    messages.success(request, 'Volunteer deleted successfully!')
    return redirect('dashboard:manage_volunteers')

@staff_member_required(login_url='dashboard:login')
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'dashboard/contact_detail.html', {'contact': contact})

@staff_member_required(login_url='dashboard:login')
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, 'Message deleted successfully!')
    return redirect('dashboard:manage_contacts')

@staff_member_required(login_url='dashboard:login')
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'dashboard/payment_detail.html', {'payment': payment})

@staff_member_required(login_url='dashboard:login')
def registration_detail(request, pk):
    registration = get_object_or_404(FeedingRegistration, pk=pk)
    return render(request, 'dashboard/registration_detail.html', {'registration': registration})

@staff_member_required(login_url='dashboard:login')
def delete_registration(request, pk):
    registration = get_object_or_404(FeedingRegistration, pk=pk)
    registration.delete()
    messages.success(request, 'Meal registration deleted successfully!')
    return redirect('dashboard:manage_registrations')

@staff_member_required(login_url='dashboard:login')
def manage_blog(request):
    search = request.GET.get('search', '')
    posts = BlogPost.objects.all()
    if search:
        posts = posts.filter(
            models.Q(title__icontains=search) |
            models.Q(summary__icontains=search)
        )
    paginator = Paginator(posts, 10)
    posts_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_blog.html', {
        'posts': posts_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_blog(request):
    from dashboard.forms import BlogPostForm
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('dashboard:manage_blog')
    else:
        form = BlogPostForm()
    return render(request, 'dashboard/create_blog.html', {'form': form})

@staff_member_required(login_url='dashboard:login')
def edit_blog(request, pk):
    from dashboard.forms import BlogPostForm
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('dashboard:manage_blog')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'dashboard/create_blog.html', {'form': form, 'post': post})

@staff_member_required(login_url='dashboard:login')
def delete_blog(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.delete()
    messages.success(request, 'Blog post deleted successfully!')
    return redirect('dashboard:manage_blog')

@staff_member_required(login_url='dashboard:login')
def send_email_to_subscribers(request):
    subscribers = Subscriber.objects.all()
    count = subscribers.count()

    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not subject or not message:
            messages.error(request, 'Subject and message are required.')
        elif count == 0:
            messages.error(request, 'No subscribers to send to.')
        else:
            try:
                emails = [(subject, message, settings.DEFAULT_FROM_EMAIL, [s.email]) for s in subscribers]
                from django.core.mail import send_mass_mail
                send_mass_mail(emails, fail_silently=False)
                messages.success(request, f'Email sent successfully to {count} subscribers!')
            except Exception as e:
                messages.error(request, f'Failed to send emails: {str(e)}')

    return render(request, 'dashboard/send_email.html', {'subscriber_count': count})

# Newsletter Management Views
@staff_member_required(login_url='dashboard:login')
def manage_newsletters(request):
    search = request.GET.get('search', '')
    newsletters = Newsletter.objects.all().order_by('-created_at')
    if search:
        newsletters = newsletters.filter(
            models.Q(title__icontains=search) |
            models.Q(subject__icontains=search)
        )
    paginator = Paginator(newsletters, 10)
    newsletters_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_newsletters.html', {
        'newsletters': newsletters_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.created_at = timezone.now()
            
            # Just save the newsletter - don't send emails automatically
            # Email sending is disabled to use this system for blog publishing only
            if newsletter.status == 'sent':
                newsletter.sent_at = timezone.now()
                newsletter.recipients_count = 0  # Set to 0 since we're not sending emails
                messages.success(request, f'Blog post "{newsletter.title}" published successfully!')
            else:
                messages.success(request, f'Blog post "{newsletter.title}" saved as draft!')
            
            newsletter.save()
            return redirect('dashboard:manage_newsletters')
    else:
        form = NewsletterForm()
    return render(request, 'dashboard/create_newsletter.html', {'form': form})

@staff_member_required(login_url='dashboard:login')
def edit_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES, instance=newsletter)
        if form.is_valid():
            newsletter = form.save(commit=False)
            
            # Just save the newsletter - don't send emails automatically
            # Email sending is disabled to use this system for blog publishing only
            if newsletter.status == 'sent' and not newsletter.sent_at:
                newsletter.sent_at = timezone.now()
                newsletter.recipients_count = 0  # Set to 0 since we're not sending emails
                messages.success(request, f'Blog post "{newsletter.title}" published successfully!')
            else:
                messages.success(request, f'Blog post "{newsletter.title}" updated successfully!')
            
            newsletter.save()
            return redirect('dashboard:manage_newsletters')
    else:
        form = NewsletterForm(instance=newsletter)
    return render(request, 'dashboard/edit_newsletter.html', {'form': form, 'newsletter': newsletter})

@staff_member_required(login_url='dashboard:login')
def newsletter_detail(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, 'dashboard/newsletter_detail.html', {'newsletter': newsletter})

@staff_member_required(login_url='dashboard:login')
def preview_newsletter(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    return render(request, 'dashboard/newsletter_preview.html', {'newsletter': newsletter})

def send_newsletter(newsletter):
    """Helper function to send newsletter to all subscribers"""
    try:
        subscribers = Subscriber.objects.all()
        if not subscribers.exists():
            return False
        
        # Prepare email data
        email_messages = []
        for subscriber in subscribers:
            email_messages.append((
                newsletter.subject,
                newsletter.content,
                settings.DEFAULT_FROM_EMAIL,
                [subscriber.email]
            ))
        
        # Send mass email
        send_mass_mail(email_messages, fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending newsletter: {e}")
        return False

@staff_member_required(login_url='dashboard:login')
def manage_subscribers(request):
    search = request.GET.get('search', '')
    subscribers = Subscriber.objects.all().order_by('-subscribed_at')
    if search:
        subscribers = subscribers.filter(email__icontains=search)
    paginator = Paginator(subscribers, 20)
    subscribers_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_subscribers.html', {
        'subscribers': subscribers_paginated,
        'total': Subscriber.objects.count(),
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def export_subscribers(request):
    import csv
    from django.http import HttpResponse
    from datetime import datetime
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="subscribers_{timestamp}.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    writer.writerow(['Email', 'Subscribed Date', 'Subscribed Time'])
    
    # Write subscriber data
    subscribers = Subscriber.objects.all().order_by('-subscribed_at')
    for subscriber in subscribers:
        writer.writerow([
            subscriber.email,
            subscriber.subscribed_at.strftime('%Y-%m-%d'),
            subscriber.subscribed_at.strftime('%H:%M:%S')
        ])
    
    return response

@staff_member_required(login_url='dashboard:login')
def manage_renovations(request):
    renovations = HouseRenovation.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_renovations.html', {'renovations': renovations})

@staff_member_required(login_url='dashboard:login')
def create_renovation(request):
    from dashboard.forms import HouseRenovationForm
    if request.method == 'POST':
        form = HouseRenovationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Renovation added successfully!')
            return redirect('dashboard:manage_renovations')
    else:
        form = HouseRenovationForm()
    return render(request, 'dashboard/renovation_form.html', {'form': form, 'title': 'Add Renovation'})

@staff_member_required(login_url='dashboard:login')
def edit_renovation(request, pk):
    from dashboard.forms import HouseRenovationForm
    renovation = get_object_or_404(HouseRenovation, pk=pk)
    if request.method == 'POST':
        form = HouseRenovationForm(request.POST, request.FILES, instance=renovation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Renovation updated successfully!')
            return redirect('dashboard:manage_renovations')
    else:
        form = HouseRenovationForm(instance=renovation)
    return render(request, 'dashboard/renovation_form.html', {'form': form, 'title': 'Edit Renovation', 'renovation': renovation})

@staff_member_required(login_url='dashboard:login')
def delete_renovation(request, pk):
    renovation = get_object_or_404(HouseRenovation, pk=pk)
    renovation.delete()
    messages.success(request, 'Renovation deleted successfully!')
    return redirect('dashboard:manage_renovations')

@staff_member_required(login_url='dashboard:login')
def manage_stories(request):
    search = request.GET.get('search', '')
    stories = Story.objects.all().order_by('order', '-created_at')
    if search:
        stories = stories.filter(
            models.Q(name__icontains=search) |
            models.Q(title__icontains=search) |
            models.Q(tag__icontains=search)
        )
    paginator = Paginator(stories, 10)
    stories_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_stories.html', {
        'stories': stories_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_story(request):
    from dashboard.forms import StoryForm
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Story created successfully!')
            return redirect('dashboard:manage_stories')
    else:
        form = StoryForm()
    return render(request, 'dashboard/story_form.html', {'form': form, 'title': 'Add New Story'})

@staff_member_required(login_url='dashboard:login')
def edit_story(request, pk):
    from dashboard.forms import StoryForm
    story = get_object_or_404(Story, pk=pk)
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES, instance=story)
        if form.is_valid():
            form.save()
            messages.success(request, 'Story updated successfully!')
            return redirect('dashboard:manage_stories')
    else:
        form = StoryForm(instance=story)
    return render(request, 'dashboard/story_form.html', {'form': form, 'title': 'Edit Story', 'story': story})

@staff_member_required(login_url='dashboard:login')
def delete_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    story.delete()
    messages.success(request, 'Story deleted successfully!')
    return redirect('dashboard:manage_stories')

@staff_member_required(login_url='dashboard:login')
def manage_packages(request):
    search = request.GET.get('search', '')
    packages = DonationPackage.objects.all().order_by('order', 'amount')
    if search:
        packages = packages.filter(
            models.Q(title__icontains=search) |
            models.Q(description__icontains=search)
        )
    paginator = Paginator(packages, 10)
    packages_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_packages.html', {
        'packages': packages_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_package(request):
    from dashboard.forms import DonationPackageForm
    if request.method == 'POST':
        form = DonationPackageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation package created successfully!')
            return redirect('dashboard:manage_packages')
    else:
        form = DonationPackageForm()
    return render(request, 'dashboard/package_form.html', {'form': form, 'title': 'Add New Package'})

@staff_member_required(login_url='dashboard:login')
def edit_package(request, pk):
    from dashboard.forms import DonationPackageForm
    package = get_object_or_404(DonationPackage, pk=pk)
    if request.method == 'POST':
        form = DonationPackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation package updated successfully!')
            return redirect('dashboard:manage_packages')
    else:
        form = DonationPackageForm(instance=package)
    return render(request, 'dashboard/package_form.html', {'form': form, 'title': 'Edit Package', 'package': package})

@staff_member_required(login_url='dashboard:login')
def delete_package(request, pk):
    package = get_object_or_404(DonationPackage, pk=pk)
    package.delete()
    messages.success(request, 'Donation package deleted successfully!')
    return redirect('dashboard:manage_packages')

@staff_member_required(login_url='dashboard:login')
def manage_champions(request):
    search = request.GET.get('search', '')
    champions = Champion.objects.all().order_by('order', '-created_at')
    if search:
        champions = champions.filter(
            models.Q(name__icontains=search) |
            models.Q(role__icontains=search)
        )
    paginator = Paginator(champions, 10)
    champions_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_champions.html', {
        'champions': champions_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_champion(request):
    from dashboard.forms import ChampionForm
    if request.method == 'POST':
        form = ChampionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Champion story created successfully!')
            return redirect('dashboard:manage_champions')
    else:
        form = ChampionForm()
    return render(request, 'dashboard/champion_form.html', {'form': form, 'title': 'Add New Champion'})

@staff_member_required(login_url='dashboard:login')
def edit_champion(request, pk):
    from dashboard.forms import ChampionForm
    champion = get_object_or_404(Champion, pk=pk)
    if request.method == 'POST':
        form = ChampionForm(request.POST, request.FILES, instance=champion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Champion story updated successfully!')
            return redirect('dashboard:manage_champions')
    else:
        form = ChampionForm(instance=champion)
    return render(request, 'dashboard/champion_form.html', {'form': form, 'title': 'Edit Champion', 'champion': champion})

@staff_member_required(login_url='dashboard:login')
def delete_champion(request, pk):
    champion = get_object_or_404(Champion, pk=pk)
    champion.delete()
    messages.success(request, 'Champion story deleted successfully!')
    return redirect('dashboard:manage_champions')

@staff_member_required(login_url='dashboard:login')
def manage_gallery(request):
    search = request.GET.get('search', '')
    images = GalleryImage.objects.all().order_by('order', '-created_at')
    if search:
        images = images.filter(
            models.Q(title__icontains=search) |
            models.Q(caption__icontains=search)
        )
    paginator = Paginator(images, 12)
    images_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_gallery.html', {
        'gallery_images': images_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_gallery_image(request):
    from dashboard.forms import GalleryImageForm
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery image added successfully!')
            return redirect('dashboard:manage_gallery')
    else:
        form = GalleryImageForm()
    return render(request, 'dashboard/gallery_form.html', {'form': form, 'title': 'Add Gallery Image'})

@staff_member_required(login_url='dashboard:login')
def edit_gallery_image(request, pk):
    from dashboard.forms import GalleryImageForm
    image = get_object_or_404(GalleryImage, pk=pk)
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery image updated successfully!')
            return redirect('dashboard:manage_gallery')
    else:
        form = GalleryImageForm(instance=image)
    return render(request, 'dashboard/gallery_form.html', {'form': form, 'title': 'Edit Gallery Image', 'gallery_image': image})

@staff_member_required(login_url='dashboard:login')
def delete_gallery_image(request, pk):
    image = get_object_or_404(GalleryImage, pk=pk)
    image.delete()
    messages.success(request, 'Gallery image deleted successfully!')
    return redirect('dashboard:manage_gallery')

# Milestone Management Views
@staff_member_required(login_url='dashboard:login')
def manage_milestones(request):
    from rotom.models import Milestone
    search = request.GET.get('search', '')
    milestones = Milestone.objects.all().order_by('order', 'year')
    if search:
        milestones = milestones.filter(
            models.Q(year__icontains=search) |
            models.Q(title__icontains=search) |
            models.Q(description__icontains=search)
        )
    paginator = Paginator(milestones, 12)
    milestones_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_milestones.html', {
        'milestones': milestones_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_milestone(request):
    from dashboard.forms import MilestoneForm
    if request.method == 'POST':
        form = MilestoneForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Milestone added successfully!')
            return redirect('dashboard:manage_milestones')
    else:
        form = MilestoneForm()
    return render(request, 'dashboard/milestone_form.html', {'form': form, 'title': 'Add Milestone'})

@staff_member_required(login_url='dashboard:login')
def edit_milestone(request, pk):
    from dashboard.forms import MilestoneForm
    from rotom.models import Milestone
    milestone = get_object_or_404(Milestone, pk=pk)
    if request.method == 'POST':
        form = MilestoneForm(request.POST, request.FILES, instance=milestone)
        if form.is_valid():
            form.save()
            messages.success(request, 'Milestone updated successfully!')
            return redirect('dashboard:manage_milestones')
    else:
        form = MilestoneForm(instance=milestone)
    return render(request, 'dashboard/milestone_form.html', {'form': form, 'title': 'Edit Milestone', 'milestone': milestone})

@staff_member_required(login_url='dashboard:login')
def delete_milestone(request, pk):
    from rotom.models import Milestone
    milestone = get_object_or_404(Milestone, pk=pk)
    milestone.delete()
    messages.success(request, 'Milestone deleted successfully!')
    return redirect('dashboard:manage_milestones')

# Team Member Management Views
@staff_member_required(login_url='dashboard:login')
def manage_team(request):
    from rotom.models import TeamMember
    search = request.GET.get('search', '')
    team_members = TeamMember.objects.all().order_by('order', 'name')
    if search:
        team_members = team_members.filter(
            models.Q(name__icontains=search) |
            models.Q(position__icontains=search)
        )
    paginator = Paginator(team_members, 12)
    team_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_team.html', {
        'team_members': team_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_team_member(request):
    from dashboard.forms import TeamMemberForm
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added successfully!')
            return redirect('dashboard:manage_team')
    else:
        form = TeamMemberForm()
    return render(request, 'dashboard/team_form.html', {'form': form, 'title': 'Add Team Member'})

@staff_member_required(login_url='dashboard:login')
def edit_team_member(request, pk):
    from dashboard.forms import TeamMemberForm
    from rotom.models import TeamMember
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated successfully!')
            return redirect('dashboard:manage_team')
    else:
        form = TeamMemberForm(instance=member)
    return render(request, 'dashboard/team_form.html', {'form': form, 'title': 'Edit Team Member', 'team_member': member})

@staff_member_required(login_url='dashboard:login')
def delete_team_member(request, pk):
    from rotom.models import TeamMember
    member = get_object_or_404(TeamMember, pk=pk)
    member.delete()
    messages.success(request, 'Team member deleted successfully!')
    return redirect('dashboard:manage_team')

# Center Photo Management Views
@staff_member_required(login_url='dashboard:login')
def manage_center_photos(request):
    from rotom.models import CenterPhoto
    search = request.GET.get('search', '')
    photos = CenterPhoto.objects.all().order_by('order', 'title')
    if search:
        photos = photos.filter(
            models.Q(title__icontains=search) |
            models.Q(description__icontains=search)
        )
    paginator = Paginator(photos, 12)
    photos_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_center_photos.html', {
        'center_photos': photos_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_center_photo(request):
    from dashboard.forms import CenterPhotoForm
    if request.method == 'POST':
        form = CenterPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Center photo added successfully!')
            return redirect('dashboard:manage_center_photos')
    else:
        form = CenterPhotoForm()
    return render(request, 'dashboard/center_photo_form.html', {'form': form, 'title': 'Add Center Photo'})

@staff_member_required(login_url='dashboard:login')
def edit_center_photo(request, pk):
    from dashboard.forms import CenterPhotoForm
    from rotom.models import CenterPhoto
    photo = get_object_or_404(CenterPhoto, pk=pk)
    if request.method == 'POST':
        form = CenterPhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Center photo updated successfully!')
            return redirect('dashboard:manage_center_photos')
    else:
        form = CenterPhotoForm(instance=photo)
    return render(request, 'dashboard/center_photo_form.html', {'form': form, 'title': 'Edit Center Photo', 'center_photo': photo})

@staff_member_required(login_url='dashboard:login')
def delete_center_photo(request, pk):
    from rotom.models import CenterPhoto
    photo = get_object_or_404(CenterPhoto, pk=pk)
    photo.delete()
    messages.success(request, 'Center photo deleted successfully!')
    return redirect('dashboard:manage_center_photos')


# Partner Management Views
@staff_member_required(login_url='dashboard:login')
def manage_partners(request):
    from rotom.models import Partner
    search = request.GET.get('search', '')
    partners = Partner.objects.all().order_by('order', 'name')
    if search:
        partners = partners.filter(
            models.Q(name__icontains=search) |
            models.Q(description__icontains=search)
        )
    paginator = Paginator(partners, 15)
    partners_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_partners.html', {
        'partners': partners_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_partner(request):
    from dashboard.forms import PartnerForm
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Partner added successfully!')
            return redirect('dashboard:manage_partners')
    else:
        form = PartnerForm()
    return render(request, 'dashboard/partner_form.html', {'form': form, 'title': 'Add New Partner'})

@staff_member_required(login_url='dashboard:login')
def edit_partner(request, pk):
    from dashboard.forms import PartnerForm
    from rotom.models import Partner
    partner = get_object_or_404(Partner, pk=pk)
    if request.method == 'POST':
        form = PartnerForm(request.POST, request.FILES, instance=partner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Partner updated successfully!')
            return redirect('dashboard:manage_partners')
    else:
        form = PartnerForm(instance=partner)
    return render(request, 'dashboard/partner_form.html', {'form': form, 'title': 'Edit Partner', 'partner': partner})

@staff_member_required(login_url='dashboard:login')
def delete_partner(request, pk):
    from rotom.models import Partner
    partner = get_object_or_404(Partner, pk=pk)
    partner.delete()
    messages.success(request, 'Partner deleted successfully!')
    return redirect('dashboard:manage_partners')


# Testimonial Management Views
@staff_member_required(login_url='dashboard:login')
def manage_testimonials(request):
    search = request.GET.get('search', '')
    testimonials = Testimonial.objects.all().order_by('order', '-created_at')
    if search:
        testimonials = testimonials.filter(
            models.Q(name__icontains=search) |
            models.Q(role__icontains=search) |
            models.Q(quote__icontains=search)
        )
    paginator = Paginator(testimonials, 10)
    testimonials_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_testimonials.html', {
        'testimonials': testimonials_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_testimonial(request):
    from dashboard.forms import TestimonialForm
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial added successfully!')
            return redirect('dashboard:manage_testimonials')
    else:
        form = TestimonialForm()
    return render(request, 'dashboard/testimonial_form.html', {'form': form, 'title': 'Add New Testimonial'})

@staff_member_required(login_url='dashboard:login')
def edit_testimonial(request, pk):
    from dashboard.forms import TestimonialForm
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, 'Testimonial updated successfully!')
            return redirect('dashboard:manage_testimonials')
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'dashboard/testimonial_form.html', {'form': form, 'title': 'Edit Testimonial', 'testimonial': testimonial})

@staff_member_required(login_url='dashboard:login')
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully!')
    return redirect('dashboard:manage_testimonials')


# Volunteer Gallery Management Views
@staff_member_required(login_url='dashboard:login')
def manage_volunteer_gallery(request):
    search = request.GET.get('search', '')
    images = VolunteerGallery.objects.all().order_by('order', '-created_at')
    if search:
        images = images.filter(
            models.Q(title__icontains=search)
        )
    paginator = Paginator(images, 12)
    images_paginated = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard/manage_volunteer_gallery.html', {
        'gallery_images': images_paginated,
        'search': search,
    })

@staff_member_required(login_url='dashboard:login')
def create_volunteer_gallery_image(request):
    from dashboard.forms import VolunteerGalleryForm
    if request.method == 'POST':
        form = VolunteerGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Volunteer gallery image added successfully!')
            return redirect('dashboard:manage_volunteer_gallery')
    else:
        form = VolunteerGalleryForm()
    return render(request, 'dashboard/volunteer_gallery_form.html', {'form': form, 'title': 'Add Volunteer Gallery Image'})

@staff_member_required(login_url='dashboard:login')
def edit_volunteer_gallery_image(request, pk):
    from dashboard.forms import VolunteerGalleryForm
    image = get_object_or_404(VolunteerGallery, pk=pk)
    if request.method == 'POST':
        form = VolunteerGalleryForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Volunteer gallery image updated successfully!')
            return redirect('dashboard:manage_volunteer_gallery')
    else:
        form = VolunteerGalleryForm(instance=image)
    return render(request, 'dashboard/volunteer_gallery_form.html', {'form': form, 'title': 'Edit Volunteer Gallery Image', 'gallery_image': image})

@staff_member_required(login_url='dashboard:login')
def delete_volunteer_gallery_image(request, pk):
    image = get_object_or_404(VolunteerGallery, pk=pk)
    image.delete()
    messages.success(request, 'Volunteer gallery image deleted successfully!')
    return redirect('dashboard:manage_volunteer_gallery')
