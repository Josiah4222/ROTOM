import uuid
from functools import wraps

from django.urls import reverse
import requests
import logging
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.cache import cache
from django.http import JsonResponse
from .models import Event, Payment, PreviousEvent, InterestCategory, Newsletter, SiteContent
from .forms import ContactForm, FeedingRegistrationForm, SubscriberForm, VolunteerProfileForm
from django.utils import timezone

logger = logging.getLogger(__name__)


def _page_content(page):
    """Return a dict of all SiteContent values for a page, keyed by content key."""
    return {obj.key: obj.value for obj in SiteContent.objects.filter(page=page)}


def content_check(request):
    """Return the latest SiteContent update timestamp as JSON."""
    from django.db.models import Max
    latest = SiteContent.objects.aggregate(Max('updated_at'))
    ts = latest['updated_at__max']
    return JsonResponse({'updated_at': ts.isoformat() if ts else None})


def rate_limit(key_prefix, limit=5, period=60):
    """Simple rate limiting decorator. Limits requests per IP."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method == 'POST':
                ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
                if ',' in ip:
                    ip = ip.split(',')[0].strip()
                cache_key = f"rate_limit:{key_prefix}:{ip}"
                requests_count = cache.get(cache_key, 0)
                
                if requests_count >= limit:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': 'Too many requests. Please try again later.'}, status=429)
                    messages.error(request, 'Too many requests. Please try again later.')
                    return redirect(request.path)
                
                cache.set(cache_key, requests_count + 1, period)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@rate_limit('contact', limit=5, period=300)  # 5 submissions per 5 minutes
def home(request):
    from rotom.models import Partner
    partners = Partner.objects.filter(is_active=True).order_by('order', 'name')
    content = _page_content('home')
    navbar_content = _page_content('navbar')
    
    if request.method == 'POST':
        logger.info(f"POST data: {request.POST}")
        form = ContactForm(request.POST)
        if form.is_valid():
            logger.info(f"Form valid, saving: {form.cleaned_data}")
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True}, status=200)
            return render(request, 'rotom/index.html', {
                'form': ContactForm(),
                'partners': partners,
                'content': content,
                'navbar_content': navbar_content,
                'success_message': 'Thank you for your message! We will get back to you soon.'
            })
        else:
            logger.warning(f"Contact form errors: {form.errors}, POST data: {request.POST}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            return render(request, 'rotom/index.html', {'form': form, 'partners': partners, 'content': content, 'navbar_content': navbar_content})
    else:
        form = ContactForm()
    return render(request, 'rotom/index.html', {'form': form, 'partners': partners, 'content': content, 'navbar_content': navbar_content})

def subscribe(request):
    if request.method == 'POST':
        logger.info(f"Subscribe form POST data: {request.POST}")
        form = SubscriberForm(request.POST)
        if form.is_valid():
            logger.info(f"Subscribe form valid, saving: {form.cleaned_data}")
            subscriber = form.save()
            # Send welcome email
            try:
                send_mail(
                    subject='Welcome to ROTOM Ethiopia Newsletter!',
                    message=f'Thank you for subscribing, {subscriber.email}! Stay tuned for updates.',
                    from_email='rotomethiopia@reachone-touchone.org',
                    recipient_list=[subscriber.email],
                    fail_silently=False,
                )
                logger.info(f"Welcome email sent to {subscriber.email}")
            except Exception as e:
                logger.error(f"Failed to send welcome email to {subscriber.email}: {e}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'}, status=200)
            messages.success(request, 'Thank you for subscribing!')
            return render(request, request.path, {'subscribe_form': SubscriberForm()})
        else:
            logger.warning(f"Subscribe form errors: {form.errors}, POST data: {request.POST}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            messages.error(request, 'Please enter a valid email address.')
    return render(request, request.path, {'subscribe_form': form})

def journies(request):
    return render(request, 'rotom/journies.html')

def achievements(request):
    return render(request, 'rotom/achievements.html')

def centerbased(request):
    from rotom.models import CenterPhoto
    center_photos = CenterPhoto.objects.filter(is_active=True).order_by('order', 'title')
    content = _page_content('centerbased')
    navbar_content = _page_content('navbar')
    return render(request, 'rotom/centerbased.html', {'center_photos': center_photos, 'content': content, 'navbar_content': navbar_content})

def homebased(request):
    from .models import HouseRenovation
    renovations = HouseRenovation.objects.all()
    content = _page_content('homebased')
    navbar_content = _page_content('navbar')
    return render(request, 'rotom/homebased.html', {'renovations': renovations, 'content': content, 'navbar_content': navbar_content})

def ourstory(request):
    from rotom.models import Milestone, TeamMember
    milestones = Milestone.objects.filter(is_active=True).order_by('order', 'year')
    team_members = TeamMember.objects.filter(is_active=True).order_by('order', 'name')
    content = _page_content('about')
    navbar_content = _page_content('navbar')
    return render(request, 'rotom/ourstory.html', {
        'milestones': milestones,
        'team_members': team_members,
        'content': content,
        'navbar_content': navbar_content,
    })

def ourplan(request):
    return render(request, 'rotom/ourplan.html')

# rotom/views.py (updated volunteer view to handle errors properly)
def volunteer(request):
    if request.method == 'POST':
        form = VolunteerProfileForm(request.POST)
        if form.is_valid():
            volunteer = form.save()
            # Optionally save M2M fields if handled separately, but ModelForm does it
            messages.success(request, 'You have been registered! Our team will contact you soon.')
            return redirect('volunteer')  # Redirect to same page to show success message
        else:
            # Log errors for debugging
            logger.warning(f"Volunteer form errors: {form.errors}")
            messages.error(request, 'Please correct the errors below to complete your registration.')
    else:
        form = VolunteerProfileForm()
    
    all_interest_options = InterestCategory.objects.all()
    content = _page_content('volunteer')
    navbar_content = _page_content('navbar')
    return render(request, 'rotom/volunteer.html', {
        'form': form, 
        'all_interest_options': all_interest_options,
        'content': content,
        'navbar_content': navbar_content,
    })
def events_view(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(event_date__gte=now).select_related().order_by('event_date')
    previous_photos = PreviousEvent.objects.select_related().order_by('-event_date')
    return render(request, 'rotom/events.html', {
        'upcoming_events': upcoming_events,
        'previous_photos': previous_photos
    })


def event_detail(request, event_id):
    from django.shortcuts import get_object_or_404
    event = get_object_or_404(Event, id=event_id)
    # Get other upcoming events for sidebar
    now = timezone.now()
    other_events = Event.objects.filter(event_date__gte=now).exclude(id=event_id).order_by('event_date')[:3]
    return render(request, 'rotom/event_detail.html', {
        'event': event,
        'other_events': other_events
    })

# rotom/views.py (updated donate function to pass tx_ref in return_url)
# rotom/views.py (updated donate function to pass tx_ref in return_url)
@rate_limit('donate', limit=10, period=300)  # 10 donations per 5 minutes
def donate(request):
    from rotom.models import DonationPackage
    packages = DonationPackage.objects.filter(is_active=True).order_by('order')
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number', '')

        logger.info(f"Received donation form: amount={amount}, email={email}, first_name={first_name}, last_name={last_name}, phone_number={phone_number}")

        # Validate input
        try:
            amount = float(amount)
            if amount < 50:  # Changed from 100 to 50
                messages.error(request, 'Minimum donation amount is 50 ETB.')
                logger.warning(f"Invalid amount: {amount}")
                return redirect('donate')
        except ValueError:
            messages.error(request, 'Invalid amount entered.')
            logger.warning(f"ValueError for amount: {amount}")
            return redirect('donate')

        # Validate email
        if not email or '@' not in email or '.' not in email:
            messages.error(request, 'Please provide a valid email address.')
            logger.warning(f"Invalid email: {email}")
            return redirect('donate')

        # Validate names
        if not first_name or not last_name:
            messages.error(request, 'First and last names are required.')
            logger.warning(f"Missing names: first_name={first_name}, last_name={last_name}")
            return redirect('donate')

        # Validate phone number (if provided)
        if phone_number and (not (phone_number.startswith('09') or phone_number.startswith('07')) or len(phone_number) != 10):
            messages.error(request, 'Phone number must be 10 digits starting with 09 or 07.')
            logger.warning(f"Invalid phone number: {phone_number}")
            return redirect('donate')

        # Generate unique transaction reference
        tx_ref = f"ROTOM-{uuid.uuid4()}"

        # Save payment to database
        payment = Payment.objects.create(
            amount=amount,
            tx_ref=tx_ref,
            status='pending',
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )

        # Chapa API endpoint
        url = 'https://api.chapa.co/v1/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            'amount': str(amount),
            'currency': 'ETB',
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'tx_ref': tx_ref,
            'callback_url': request.build_absolute_uri(reverse('payment_callback')),
            'return_url': request.build_absolute_uri(reverse('payment_success') + f'?tx_ref={tx_ref}'),
            'customization': {
                'title': 'ROTOM Donation',
                'description': 'Support our seniors in Ethiopia'
            }
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            logger.info(f"Chapa API response: status={response.status_code}, data={response_data}")

            if response_data.get('status') == 'success':
                checkout_url = response_data['data']['checkout_url']
                logger.info(f"Redirecting to Chapa checkout: {checkout_url}")
                return redirect(checkout_url)
            else:
                error_message = response_data.get('message', 'Unknown error')
                messages.error(request, f'Failed to initiate payment: {error_message}')
                payment.status = 'failed'
                payment.save()
                logger.error(f"Chapa API error: {error_message}")
                return redirect('donate')
        except requests.RequestException as e:
            messages.error(request, f'Error connecting to Chapa: {str(e)}')
            payment.status = 'failed'
            payment.save()
            logger.error(f"Chapa request exception: {str(e)}")
            return redirect('donate')

    return render(request, 'rotom/donation.html', {'packages': packages})

def payment_callback(request):
    tx_ref = request.GET.get('tx_ref')
    status = request.GET.get('status')

    logger.info(f"Payment callback received: tx_ref={tx_ref}, status={status}")

    if tx_ref:
        try:
            payment = Payment.objects.get(tx_ref=tx_ref)
            
            # Verify transaction with Chapa API
            try:
                url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
                headers = {'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'}
                response = requests.get(url, headers=headers)
                response_data = response.json()
                logger.info(f"Chapa verify response: {response_data}")

                # Check the actual transaction status from Chapa
                chapa_status = response_data.get('data', {}).get('status', '').lower()
                
                if chapa_status == 'success':
                    payment.status = 'success'
                    payment.save()
                    logger.info(f"Payment {tx_ref} marked as success")
                elif 'failed' in chapa_status or 'cancel' in chapa_status:
                    # Handles: 'failed', 'cancelled', 'canceled', 'failed/cancelled', etc.
                    payment.status = 'failed'
                    payment.save()
                    logger.warning(f"Payment {tx_ref} marked as failed (Chapa status: {chapa_status})")
                else:
                    # Keep as pending if status is unclear
                    logger.warning(f"Payment {tx_ref} has unclear status: {chapa_status}")
                    
            except Exception as e:
                logger.error(f"Error verifying payment with Chapa: {str(e)}")
                
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for tx_ref: {tx_ref}")
        except Exception as e:
            logger.error(f"Error in payment callback: {str(e)}")

    return redirect('payment_success')



def take_action(request):
    if request.method == "POST":
        form = FeedingRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 
                "Thank you for registering! We will contact you to confirm your feeding schedule. / "
                "ለመመዝገብዎ እናመሰግናለን! የመመገቢያ መርሃግዎን ለማረጋገጥ እንገንዘብዎታለን።"
            )
            # Redirect with anchor to keep user at the form section
            return redirect(reverse('take_action') + '#feeding-form-section')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeedingRegistrationForm()
    
    content = _page_content('takeaction')
    navbar_content = _page_content('navbar')
    context = {
        'form': form,
        'content': content,
        'navbar_content': navbar_content,
    }
    return render(request, 'rotom/take_action.html', context)

def payment_success(request):
    tx_ref = request.GET.get('tx_ref')
    
    if not tx_ref:
        return render(request, 'rotom/payment_success.html', {'status': 'unknown'})
    
    try:
        payment = Payment.objects.get(tx_ref=tx_ref)
        
        # If payment is still pending, try to verify it with Chapa
        if payment.status == 'pending':
            try:
                url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
                headers = {'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'}
                response = requests.get(url, headers=headers)
                response_data = response.json()
                logger.info(f"Payment success page - Chapa verify response: {response_data}")
                
                # Check the actual transaction status from Chapa
                chapa_status = response_data.get('data', {}).get('status', '').lower()
                
                if chapa_status == 'success':
                    payment.status = 'success'
                    payment.save()
                    logger.info(f"Payment {tx_ref} verified and marked as success")
                elif 'failed' in chapa_status or 'cancel' in chapa_status:
                    # Handles: 'failed', 'cancelled', 'canceled', 'failed/cancelled', etc.
                    payment.status = 'failed'
                    payment.save()
                    logger.warning(f"Payment {tx_ref} marked as failed (Chapa status: {chapa_status})")
                else:
                    logger.warning(f"Payment {tx_ref} has unclear status: {chapa_status}")
                    
            except Exception as e:
                logger.error(f"Error verifying payment on success page: {str(e)}")
        
        context = {'tx_ref': tx_ref, 'status': payment.status, 'amount': payment.amount}
    except Payment.DoesNotExist:
        logger.error(f"Payment not found for tx_ref: {tx_ref}")
        context = {'tx_ref': tx_ref, 'status': 'unknown'}
    
    return render(request, 'rotom/payment_success.html', context)



def feeding_registration(request):
    if request.method == 'POST':
        form = FeedingRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the FeedingRegistration model
            messages.success(request, 'Thank you for registering! We will contact you to confirm your feeding schedule. / ለመመዝገብዎ እናመሰግናለን! የመመገቢያ መርሃግዎን ለማረጋገጥ እናገኝዎታለን።')
            return redirect('take_action')
    else:
        form = FeedingRegistrationForm()
    
    return render(request, 'rotom/take_action.html', {'form': form})




def champions(request):
    from rotom.models import Champion, GalleryImage
    champions = Champion.objects.filter(is_active=True).order_by('order', '-created_at')
    gallery_images = GalleryImage.objects.filter(is_active=True).order_by('order', '-created_at')
    content = _page_content('champions')
    navbar_content = _page_content('navbar')
    context = {
        'champions': champions,
        'gallery_images': gallery_images,
        'content': content,
        'navbar_content': navbar_content,
    }
    return render(request, 'rotom/champions.html', context)

def stories(request):
    from rotom.models import Story
    stories = Story.objects.filter(published=True).order_by('order', '-created_at')
    content = _page_content('stories')
    navbar_content = _page_content('navbar')
    return render(request, 'rotom/stories.html', {'stories': stories, 'content': content, 'navbar_content': navbar_content})

def blog(request):
    from .models import BlogPost
    from django.core.paginator import Paginator
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    paginator = Paginator(posts, 6)
    newsletters = paginator.get_page(request.GET.get('page'))
    return render(request, 'rotom/blog.html', {'newsletters': newsletters})

def blog_detail(request, post_id):
    from django.shortcuts import get_object_or_404
    from .models import BlogPost
    post = get_object_or_404(BlogPost, id=post_id, published=True)
    related_posts = BlogPost.objects.filter(published=True).exclude(id=post_id).order_by('-created_at')[:3]
    return render(request, 'rotom/blog_detail.html', {
        'newsletter': post,
        'related_posts': related_posts
    })