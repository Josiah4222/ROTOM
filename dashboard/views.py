# views.py (add edit views for Event and PreviousEvent)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.utils import timezone

from rotom.models import Contact, Event, FeedingRegistration, Payment, PreviousEvent, VolunteerProfile
from .forms import EventForm, PreviousEventForm  # Import the new form

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
    now = timezone.now()
    total_volunteers = VolunteerProfile.objects.count()
    total_events = Event.objects.filter(event_date__gte=now).count()  # Only upcoming
    total_previous_events = PreviousEvent.objects.count()
    total_payments = Payment.objects.filter(status='success').count()
    total_contacts = Contact.objects.count()
    total_registrations = FeedingRegistration.objects.count()

    recent_volunteers = VolunteerProfile.objects.all().order_by('-id')[:5]
    recent_contacts = Contact.objects.all().order_by('-created_at')[:5]
    recent_payments = Payment.objects.filter(status='success').order_by('-created_at')[:5]
    recent_registrations = FeedingRegistration.objects.all().order_by('-created_at')[:5]

    context = {
        'total_volunteers': total_volunteers,
        'total_events': total_events,
        'total_previous_events': total_previous_events,
        'total_payments': total_payments,
        'total_contacts': total_contacts,
        'total_registrations': total_registrations,
        'recent_volunteers': recent_volunteers,
        'recent_contacts': recent_contacts,
        'recent_payments': recent_payments,
        'recent_registrations': recent_registrations,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@staff_member_required(login_url='dashboard:login')
def manage_volunteers(request):
    volunteers = VolunteerProfile.objects.all().order_by('-id')
    paginator = Paginator(volunteers, 10)
    page_number = request.GET.get('page')
    volunteers_paginated = paginator.get_page(page_number)
    return render(request, 'dashboard/manage_volunteers.html', {'volunteers': volunteers_paginated})

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
def manage_events(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(event_date__gte=now).order_by('event_date')
    past_events = PreviousEvent.objects.all().order_by('-event_date')
    paginator_upcoming = Paginator(upcoming_events, 10)
    paginator_past = Paginator(past_events, 10)
    page_number = request.GET.get('page')
    upcoming_paginated = paginator_upcoming.get_page(page_number)
    past_paginated = paginator_past.get_page(page_number)
    return render(request, 'dashboard/manage_events.html', {
        'upcoming_events': upcoming_paginated,
        'past_events': past_paginated
    })

@staff_member_required(login_url='dashboard:login')
def manage_contacts(request):
    contacts = Contact.objects.all().order_by('-created_at')
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    contacts_paginated = paginator.get_page(page_number)
    return render(request, 'dashboard/manage_contacts.html', {'contacts': contacts_paginated})

# dashboard/views.py (updated manage_payments to show all for debugging)
@staff_member_required(login_url='dashboard:login')
def manage_payments(request):
    # Show all payments for debugging (change back to .filter(status='success') once fixed)
    payments = Payment.objects.all().order_by('-created_at')
    paginator = Paginator(payments, 10)
    page_number = request.GET.get('page')
    payments_paginated = paginator.get_page(page_number)
    return render(request, 'dashboard/manage_payments.html', {'payments': payments_paginated})
@staff_member_required(login_url='dashboard:login')
def manage_registrations(request):
    registrations = FeedingRegistration.objects.all().order_by('-created_at')
    paginator = Paginator(registrations, 10)
    page_number = request.GET.get('page')
    registrations_paginated = paginator.get_page(page_number)
    return render(request, 'dashboard/manage_registrations.html', {'registrations': registrations_paginated})

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