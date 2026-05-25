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

from rotom.models import Contact, Event, FeedingRegistration, Payment, PreviousEvent, VolunteerProfile, Newsletter, Subscriber, BlogPost, HouseRenovation, Story, DonationPackage, Champion, GalleryImage, Testimonial, SiteContent
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
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, 'dashboard/contact_detail.html', {'contact': contact})

@staff_member_required(login_url='dashboard:login')
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'dashboard/payment_detail.html', {'payment': payment})

@staff_member_required(login_url='dashboard:login')
def registration_detail(request, pk):
    registration = get_object_or_404(FeedingRegistration, pk=pk)
    return render(request, 'dashboard/registration_detail.html', {'registration': registration})

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


# ─── Site Content (Static Text Editor) ───────────────────────────────────────

# Default content definitions: (page, key, label, default_value)
SITE_CONTENT_DEFAULTS = [
    # ── Navbar ──────────────────────────────────────────────────────────────
    ('navbar', 'brand_name',    'Brand Name',    'ROTOM Ethiopia'),
    ('navbar', 'brand_tagline', 'Brand Tagline', 'Older persons living dignified & fulfilled lives.'),
    ('navbar', 'nav_home',      'Nav: Home',     'HOME'),
    ('navbar', 'nav_about',     'Nav: About Us', 'ABOUT US'),
    ('navbar', 'nav_stories',   'Nav: Stories',  'STORIES'),
    ('navbar', 'nav_blog',      'Nav: Blog',     'BLOG'),
    ('navbar', 'nav_takeaction','Nav: Take Action','TAKE ACTION'),
    ('navbar', 'nav_events',    'Nav: Events',   'EVENTS'),
    ('navbar', 'nav_donate',    'Nav: Donate',   'DONATE'),

    # ── Home Page ────────────────────────────────────────────────────────────
    ('home', 'hero_title',           'Hero Title',           'ROTOM-Ethiopia'),
    ('home', 'hero_subtitle',        'Hero Subtitle',        'Older persons and their dependents living dignified and fulfilling lives.'),
    ('home', 'hero_btn_discover',    'Hero Button: Discover','Discover'),
    ('home', 'hero_btn_learn',       'Hero Button: Learn More','Learn More'),
    ('home', 'impact_title',         'Impact Section Title', 'Our Impact'),
    ('home', 'impact_stat1_num',     'Impact Stat 1: Number','120+'),
    ('home', 'impact_stat1_label',   'Impact Stat 1: Label', 'Elders Reached'),
    ('home', 'impact_stat2_num',     'Impact Stat 2: Number','70+'),
    ('home', 'impact_stat2_label',   'Impact Stat 2: Label', 'Grandchildren & Dependents'),
    ('home', 'impact_stat3_num',     'Impact Stat 3: Number','30+'),
    ('home', 'impact_stat3_label',   'Impact Stat 3: Label', 'Seniors in Center'),
    ('home', 'impact_stat4_num',     'Impact Stat 4: Number','500+'),
    ('home', 'impact_stat4_label',   'Impact Stat 4: Label', 'Volunteers'),
    ('home', 'impact_stat5_num',     'Impact Stat 5: Number','200+'),
    ('home', 'impact_stat5_label',   'Impact Stat 5: Label', 'Indirectly Supported'),
    ('home', 'about_title',          'About Section Title',  'Our Story'),
    ('home', 'about_para1',          'About Paragraph 1',    'Reach One Touch One Mission (ROTOM) Ethiopia began in 2017, born from a deep belief in the transformative power of compassion and good deeds. Founded by a dedicated volunteer with a heart for the forgotten, our organization was built to be a lifeline for those who need it most. ROTOM Ethiopia is a fully registered civil society organization (Certificate number 3764) operating out of our main office in Bishoftu, Ethiopia.'),
    ('home', 'about_para2',          'About Paragraph 2',    'We provide holistic support to vulnerable older adults who have rendered Great Service to the Nation and their dependents, working tirelessly to elevate their dignity, improve their living conditions, and ensure they live out their years with the respect and care they deserve.'),
    ('home', 'pillars_title',        'Pillars Section Title','Our Pillars of Care'),
    ('home', 'pillars_intro',        'Pillars Intro Text',   'Our holistic, multigenerational care model relies on three essential pillars:'),
    ('home', 'pillar1_title',        'Pillar 1 Title',       'Home-Based Care'),
    ('home', 'pillar1_desc',         'Pillar 1 Description', 'We meet elders where they are, providing crucial access to medical care, safe housing, hygiene resources, monthly nutritional supplements, and livelihood support.'),
    ('home', 'pillar2_title',        'Pillar 2 Title',       'Grandchildren Support'),
    ('home', 'pillar2_desc',         'Pillar 2 Description', 'We invest in the future by delivering complete educational support to the grandchildren raised by our elderly beneficiaries.'),
    ('home', 'pillar3_title',        'Pillar 3 Title',       'Center-Based Care'),
    ('home', 'pillar3_desc',         'Pillar 3 Description', 'We provide a loving, fully-equipped residential haven for formerly homeless, abandoned, and severely ill older persons, restoring their health and dignity.'),
    ('home', 'testimonials_title',   'Testimonials Section Title','What People Say'),
    ('home', 'partners_title',       'Partners Section Title','Our Partners'),
    ('home', 'partners_intro',       'Partners Intro Text',  'A sincere thank you to our global family of partners and supporters. Whether you are an organization or an individual, your contributions provide more than just help. They foster a sense of family for our seniors and a future for their grandchildren. Thank you for standing with us to improve life for Ethiopia\'s elders.'),
    ('home', 'contact_title',        'Contact Section Title','Contact Us'),
    ('home', 'contact_get_in_touch', 'Contact: Get in Touch Heading','Get in Touch'),
    ('home', 'contact_email',        'Contact: Email',       'rotomethiopia@reachone-touchone.org'),
    ('home', 'contact_phone',        'Contact: Phone',       '+251 989707777'),
    ('home', 'contact_form_heading', 'Contact: Form Heading','Send Us a Message'),
    ('home', 'contact_map_heading',  'Contact: Map Heading', 'Find Us'),
    ('home', 'contact_map_desc',     'Contact: Map Description','Visit our center in the heart of Bishoftu'),
    ('home', 'contact_address',      'Contact: Address',     'Ethiopia, Oromiya, Bishoftu Kebele 05'),

    # ── About Us Page ────────────────────────────────────────────────────────
    ('about', 'hero_title',          'Hero Title',           'About ROTOM Ethiopia'),
    ('about', 'hero_description',    'Hero Description',     'Born from a deep belief in the transformative power of compassion and good deeds, we provide holistic support to vulnerable older adults who have rendered great service to the nation and their dependents, ensuring they live with dignity and respect.'),
    ('about', 'vision_title',        'Vision Card Title',    'Our Vision'),
    ('about', 'vision_text',         'Vision Card Text',     'A dignified & fulfilled life for older persons!'),
    ('about', 'values_title',        'Values Card Title',    'Our Values'),
    ('about', 'values_text',         'Values Card Text',     'We uphold Love Beyond Self, Honesty, Justice, Respect, Stewardship, Dignity, Teamwork, and Quality Service'),
    ('about', 'approach_title',      'Approach Card Title',  'Our Approach'),
    ('about', 'approach_text',       'Approach Card Text',   'A holistic, multi-generational model'),
    ('about', 'milestones_title',    'Milestones Section Title','Our Milestones'),
    ('about', 'milestones_subtitle', 'Milestones Subtitle',  'A timeline of growth and compassion'),
    ('about', 'team_title',          'Team Section Title',   'Our Team'),
    ('about', 'team_subtitle',       'Team Section Subtitle','The dedicated people behind our mission'),
    ('about', 'team_photo1_caption', 'Team Photo 1 Caption', 'Our Dedicated Team'),
    ('about', 'team_photo2_caption', 'Team Photo 2 Caption', 'Our Volunteers'),
    ('about', 'staff_title',         'Staff Section Title',  'Meet Our Staff'),
    ('about', 'staff_subtitle',      'Staff Section Subtitle','The passionate individuals driving our mission forward'),

    # ── Center-Based Care Page ───────────────────────────────────────────────
    ('centerbased', 'hero_title',    'Hero Title',           'Center-Based Senior Support'),
    ('centerbased', 'hero_subtitle', 'Hero Subtitle',        'Providing Comprehensive Care in a Dedicated Space'),
    ('centerbased', 'hero_btn',      'Hero Button',          'Discover Our Services'),
    ('centerbased', 'services_title','Services Section Title','Our Services'),
    ('centerbased', 'svc1_title',    'Service 1 Title',      '24/7 Care'),
    ('centerbased', 'svc1_desc',     'Service 1 Description','Round-the-clock care for seniors to ensure their safety and comfort.'),
    ('centerbased', 'svc2_title',    'Service 2 Title',      'Nutritious Meals'),
    ('centerbased', 'svc2_desc',     'Service 2 Description','Three nutritious meals daily'),
    ('centerbased', 'svc3_title',    'Service 3 Title',      'Cultural Coffee Ceremony'),
    ('centerbased', 'svc3_desc',     'Service 3 Description','Serving coffee with a cultural ceremony during lunchtime.'),
    ('centerbased', 'svc4_title',    'Service 4 Title',      'Hygiene Support'),
    ('centerbased', 'svc4_desc',     'Service 4 Description','Bathing sessions and haircuts for all seniors.'),
    ('centerbased', 'svc5_title',    'Service 5 Title',      'Medical Support'),
    ('centerbased', 'svc5_desc',     'Service 5 Description','Medical checkup for all seniors in the center'),
    ('centerbased', 'svc6_title',    'Service 6 Title',      'Burial Services'),
    ('centerbased', 'svc6_desc',     'Service 6 Description','Dignified burial services for seniors who pass away.'),
    ('centerbased', 'svc7_title',    'Service 7 Title',      'Cleanliness & Maintenance'),
    ('centerbased', 'svc7_desc',     'Service 7 Description','Regular cleaning and maintenance of the center facilities.'),
    ('centerbased', 'svc8_title',    'Service 8 Title',      'Live Stock & Gardening'),
    ('centerbased', 'svc8_desc',     'Service 8 Description','Seniors participate in gardening and livestock activities.'),
    ('centerbased', 'svc9_title',    'Service 9 Title',      'Craft Corner'),
    ('centerbased', 'svc9_desc',     'Service 9 Description','Creative crafts and activities to keep seniors engaged.'),
    ('centerbased', 'gallery_title', 'Gallery Section Title','Our Center with Photos'),

    # ── Home-Based Care Page ─────────────────────────────────────────────────
    ('homebased', 'hero_title',      'Hero Title',           'Home-Based Senior Support'),
    ('homebased', 'hero_subtitle',   'Hero Subtitle',        'Creating a Caring and Supportive Home Environment for Our Seniors'),
    ('homebased', 'scope_title',     'Scope Section Title',  'Our Scope'),
    ('homebased', 'scope_intro',     'Scope Intro Text',     'ROTOM Ethiopia provides a range of home-based support programs designed to enhance the quality of life for 80 older persons in our community:'),
    ('homebased', 'svc1_title',      'Service 1 Title',      'Physical and Emotional Support'),
    ('homebased', 'svc1_desc',       'Service 1 Description','Promoting emotional and social well-being through monthly meetings and supportive home visits.'),
    ('homebased', 'svc2_title',      'Service 2 Title',      'Health Enhancement'),
    ('homebased', 'svc2_desc',       'Service 2 Description','Offering medical services, annual health check-ups, monthly sanitation supplies, and educational resources to improve overall health.'),
    ('homebased', 'svc3_title',      'Service 3 Title',      'Income and Food Security'),
    ('homebased', 'svc3_desc',       'Service 3 Description','Providing monthly grocery support to ensure access to essential resources for older adults.'),
    ('homebased', 'svc4_title',      'Service 4 Title',      'Educational Empowerment for Grandchildren'),
    ('homebased', 'svc4_desc',       'Service 4 Description','Reducing the burden on older caregivers by supplying educational resources to empower the next generation.'),
    ('homebased', 'svc5_title',      'Service 5 Title',      'Additional Support'),
    ('homebased', 'svc5_desc',       'Service 5 Description','Facilitating home repairs, holiday packages and clothing'),
    ('homebased', 'renovation_title','Renovation Section Title','House Rebuilding & Renovation'),
    ('homebased', 'renovation_intro','Renovation Intro Text','We rebuild and renovate homes for our elderly beneficiaries, ensuring they have safe and comfortable living conditions.'),

    # ── Champions / Grandchildren Page ──────────────────────────────────────
    ('champions', 'hero_title',      'Hero Title',           'Educational Support for Grandchildren and Dependents'),
    ('champions', 'hero_subtitle',   'Hero Subtitle',        'Empowering the Younger Generation Through Education and Mentorship'),
    ('champions', 'stat1_num',       'Impact Stat 1: Number','45'),
    ('champions', 'stat1_label',     'Impact Stat 1: Label', 'Graduates'),
    ('champions', 'stat2_num',       'Impact Stat 2: Number','120'),
    ('champions', 'stat2_label',     'Impact Stat 2: Label', 'Grandchildren Supported'),
    ('champions', 'stat3_num',       'Impact Stat 3: Number','15'),
    ('champions', 'stat3_label',     'Impact Stat 3: Label', 'University Students'),
    ('champions', 'stat4_num',       'Impact Stat 4: Number','28'),
    ('champions', 'stat4_label',     'Impact Stat 4: Label', 'Employed Graduates'),
    ('champions', 'initiatives_title','Initiatives Section Title','Our Initiatives'),
    ('champions', 'initiatives_intro','Initiatives Intro Text','We run several programs to support the educational journey of grandchildren in our care.'),
    ('champions', 'init1_title',     'Initiative 1 Title',   'School Supplies'),
    ('champions', 'init1_desc',      'Initiative 1 Description','Providing notebooks, pens, uniforms, and other essential school materials.'),
    ('champions', 'init2_title',     'Initiative 2 Title',   'Tuition Support'),
    ('champions', 'init2_desc',      'Initiative 2 Description','Covering school fees and tuition costs for enrolled students.'),
    ('champions', 'init3_title',     'Initiative 3 Title',   'Mentorship Program'),
    ('champions', 'init3_desc',      'Initiative 3 Description','Connecting students with mentors who guide their academic and personal development.'),
    ('champions', 'init4_title',     'Initiative 4 Title',   'University Scholarships'),
    ('champions', 'init4_desc',      'Initiative 4 Description','Supporting outstanding students to pursue higher education at university level.'),
    ('champions', 'gallery_title',   'Gallery Section Title','Gallery'),
    ('champions', 'gallery_intro',   'Gallery Intro Text',   'Explore moments from our educational programs and the lives of our champions.'),

    # ── Stories Page ─────────────────────────────────────────────────────────
    ('stories', 'hero_title',        'Hero Title',           'Transformation Stories'),
    ('stories', 'hero_subtitle',     'Hero Subtitle',        'Witness the incredible journeys of our seniors - from struggle to hope, from isolation to community.'),
    ('stories', 'intro_title',       'Intro Section Title',  'Lives Changed Through Love'),
    ('stories', 'intro_subtitle',    'Intro Section Subtitle','Every elder who comes to ROTOM has a unique story. Here are just a few of the remarkable transformations we\'ve witnessed through the power of care, community, and compassion.'),
    ('stories', 'cta_title',         'CTA Section Title',    'Help Us Write More Success Stories'),
    ('stories', 'cta_subtitle',      'CTA Section Subtitle', 'Your support can transform the life of an elder in need.'),
    ('stories', 'cta_btn_donate',    'CTA Button: Donate',   'Donate Now'),
    ('stories', 'cta_btn_volunteer', 'CTA Button: Volunteer','Volunteer'),

    # ── Take Action Page ─────────────────────────────────────────────────────
    ('takeaction', 'hero_title',     'Hero Title',           'Take Action'),
    ('takeaction', 'hero_subtitle',  'Hero Subtitle',        'Your involvement makes a real difference in the lives of older persons and their dependents. Discover how you can contribute.'),
    ('takeaction', 'give_title',     'Give Section Title',   'Give'),
    ('takeaction', 'give_intro',     'Give Section Intro',   'Your generous contributions help us provide essential support to elders and their families. Every donation, whether items or financial support, makes a meaningful difference in their lives.'),
    ('takeaction', 'donate_items_title','Donate Items Card Title','Donate Items'),
    ('takeaction', 'donate_items_desc','Donate Items Description','Your generous donations help support our programs and the elders in our care. We are currently accepting:'),
    ('takeaction', 'donate_items_list','Donate Items List (one per line)','Non-perishable food items\nClothing for elders (clean and gently used)\nAdult diapers\nSanitary materials\nOffice supplies (paper, pens, notebooks)\nOther essentials as needed'),
    ('takeaction', 'financial_title','Financial Support Card Title','Financial Support'),
    ('takeaction', 'financial_desc', 'Financial Support Description','Your monetary donations directly fund our programs and help us reach more elders in need.'),
    ('takeaction', 'feeding_title',  'Feeding Section Title','Register to Feed Elders'),
    ('takeaction', 'feeding_intro',  'Feeding Section Intro','Join our feeding program and help provide nutritious meals to seniors in our care.'),
    ('takeaction', 'visit_title',    'Visit Section Title',  'Visit Us'),
    ('takeaction', 'visit_intro',    'Visit Section Intro',  'We warmly welcome visitors to our center. Come and see the work we do and meet the seniors we serve.'),
    ('takeaction', 'visit_hours',    'Visiting Hours',       'Monday - Friday: 9:00 AM - 5:00 PM\nSaturday: 10:00 AM - 3:00 PM'),
    ('takeaction', 'visit_phone',    'Visit Section Phone',  '+251 989707777'),
    ('takeaction', 'volunteer_title','Volunteer Section Title','Make a Difference'),
    ('takeaction', 'volunteer_intro','Volunteer Section Intro','Join our team of dedicated volunteers and help make a real difference in the lives of our seniors.'),
    ('takeaction', 'volunteer_opps', 'Volunteer Opportunities (one per line)','Daily care and companionship\nMedical and health support\nEducational tutoring for grandchildren\nEvent organization and coordination\nFundraising and awareness campaigns\nSkills training and workshops'),

    # ── Volunteer Page ───────────────────────────────────────────────────────
    ('volunteer', 'hero_title',      'Hero Title',           'Volunteer with Us'),
    ('volunteer', 'hero_subtitle',   'Hero Subtitle',        'Join our mission to support and care for seniors in Ethiopia'),
    ('volunteer', 'impact_title',    'Impact Section Title', 'Our Impact'),
    ('volunteer', 'impact1_title',   'Impact Item 1 Title',  'Daily Care'),
    ('volunteer', 'impact1_desc',    'Impact Item 1 Description','Providing essential care and support to seniors in need'),
    ('volunteer', 'impact2_title',   'Impact Item 2 Title',  'Community Building'),
    ('volunteer', 'impact2_desc',    'Impact Item 2 Description','Creating meaningful connections and fostering a sense of belonging'),
    ('volunteer', 'impact3_title',   'Impact Item 3 Title',  'Social Activities'),
    ('volunteer', 'impact3_desc',    'Impact Item 3 Description','Organizing events and activities to keep seniors engaged'),
    ('volunteer', 'gallery_title',   'Gallery Section Title','Volunteer Gallery'),
    ('volunteer', 'join_title',      'Join Section Title',   'Join Our Team'),
    ('volunteer', 'join_intro',      'Join Section Intro',   'Fill out the form below to start your volunteer journey with us'),
]


def _get_content_map(page):
    """Return a dict of {key: value} and {key_am: value_am} for a given page, with defaults filled in."""
    db_items = {obj.key: obj for obj in SiteContent.objects.filter(page=page)}
    result = {}
    for (p, key, label, default) in SITE_CONTENT_DEFAULTS:
        if p == page:
            obj = db_items.get(key)
            result[key] = obj.value if obj else default
            result[key + '_am'] = obj.value_am if obj else ''
    return result


@staff_member_required(login_url='dashboard:login')
def manage_site_content(request):
    """Overview page listing all pages with their content counts."""
    pages = {}
    for (page, key, label, default) in SITE_CONTENT_DEFAULTS:
        if page not in pages:
            pages[page] = {'label': dict(SiteContent.PAGE_CHOICES).get(page, page), 'total': 0, 'saved': 0}
        pages[page]['total'] += 1

    saved_counts = (
        SiteContent.objects.values('page')
        .annotate(count=models.Count('id'))
    )
    for row in saved_counts:
        if row['page'] in pages:
            pages[row['page']]['saved'] = row['count']

    return render(request, 'dashboard/manage_site_content.html', {'pages': pages})


@staff_member_required(login_url='dashboard:login')
def edit_page_content(request, page_slug):
    """Edit all content fields for a specific page (English + Amharic)."""
    page_choices_dict = dict(SiteContent.PAGE_CHOICES)
    if page_slug not in page_choices_dict:
        messages.error(request, 'Invalid page.')
        return redirect('dashboard:manage_site_content')

    page_label = page_choices_dict[page_slug]
    fields = [(key, label, default) for (p, key, label, default) in SITE_CONTENT_DEFAULTS if p == page_slug]

    # Load existing saved values
    existing = {obj.key: obj for obj in SiteContent.objects.filter(page=page_slug)}

    if request.method == 'POST':
        for (key, label, default) in fields:
            value = request.POST.get(key, '')
            value_am = request.POST.get(key + '_am', '')
            if key in existing:
                existing[key].value = value
                existing[key].value_am = value_am
                existing[key].save()
            else:
                SiteContent.objects.create(
                    page=page_slug, key=key, label=label,
                    value=value, value_am=value_am
                )
        messages.success(request, f'{page_label} content updated successfully!')
        return redirect('dashboard:edit_page_content', page_slug=page_slug)

    # Build form data with current values (db or default)
    form_fields = []
    for (key, label, default) in fields:
        obj = existing.get(key)
        current_value = obj.value if obj is not None else default
        current_value_am = obj.value_am if obj is not None else ''
        is_long = len(default) > 80 or '\n' in default
        form_fields.append({
            'key': key,
            'label': label,
            'value': current_value,
            'value_am': current_value_am,
            'is_long': is_long,
        })

    return render(request, 'dashboard/edit_page_content.html', {
        'page_slug': page_slug,
        'page_label': page_label,
        'form_fields': form_fields,
    })
