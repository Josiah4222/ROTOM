import uuid

from django.urls import reverse
import requests
import logging
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .models import Event, Payment, PreviousEvent,  InterestCategory
from .forms import ContactForm, FeedingRegistrationForm, SubscriberForm, VolunteerProfileForm
from django.utils import timezone

logger = logging.getLogger(__name__)

from django.http import JsonResponse

def home(request):
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
                'success_message': 'Thank you for your message! We will get back to you soon.'
            })
        else:
            logger.warning(f"Contact form errors: {form.errors}, POST data: {request.POST}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            return render(request, 'rotom/index.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'rotom/index.html', {'form': form})

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
                    from_email='noreply@rotomethiopia.org',
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
    return render(request, 'rotom/centerbased.html')

def homebased(request):
    return render(request, 'rotom/homebased.html')

def ourstory(request):
    return render(request, 'rotom/ourstory.html')

def ourplan(request):
    return render(request, 'rotom/ourplan.html')

# rotom/views.py (updated volunteer view to handle errors properly)
def volunteer(request):
    if request.method == 'POST':
        form = VolunteerProfileForm(request.POST)
        if form.is_valid():
            volunteer = form.save()
            # Optionally save M2M fields if handled separately, but ModelForm does it
            messages.success(request, 'Thank you for registering as a volunteer! We will contact you soon.')
            return redirect('home')
        else:
            # Log errors for debugging
            logger.warning(f"Volunteer form errors: {form.errors}")
    else:
        form = VolunteerProfileForm()
    
    all_interest_options = InterestCategory.objects.all()
    return render(request, 'rotom/volunteer.html', {
        'form': form, 
        'all_interest_options': all_interest_options
    })
def events_view(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(event_date__gte=now).order_by('event_date')
    previous_photos = PreviousEvent.objects.all().order_by('-event_date')
    return render(request, 'rotom/events.html', {
        'upcoming_events': upcoming_events,
        'previous_photos': previous_photos
    })

# rotom/views.py (updated donate function to pass tx_ref in return_url)
def donate(request):
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
        if phone_number and not (phone_number.startswith('09') or phone_number.startswith('07')) or len(phone_number) != 10:
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
            'amount': str(amount),  # Chapa expects amount as string
            'currency': 'ETB',
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'phone_number': phone_number,
            'tx_ref': tx_ref,
            'callback_url': request.build_absolute_uri('/payment/callback/'),
            'return_url': request.build_absolute_uri(f'/payment/success/?tx_ref={tx_ref}'),  # Pass tx_ref in return_url
            'customization': {
                'title': 'ROTOM Donation',  # 13 characters
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

    return render(request, 'rotom/donation.html')

def payment_callback(request):
    tx_ref = request.GET.get('tx_ref')
    status = request.GET.get('status')

    if tx_ref and status:
        try:
            payment = Payment.objects.get(tx_ref=tx_ref)
            if status == 'success':
                # Verify transaction with Chapa
                url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
                headers = {'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'}
                response = requests.get(url, headers=headers)
                response_data = response.json()
                logger.info(f"Chapa verify response: {response_data}")

                if response_data.get('status') == 'success':
                    payment.status = 'success'
                    payment.save()
                else:
                    payment.status = 'failed'
                    payment.save()
            else:
                payment.status = 'failed'
                payment.save()
        except Payment.DoesNotExist:
            logger.error(f"Payment not found for tx_ref: {tx_ref}")
            pass

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
    
    context = {
        'form': form,
        # Add any other context vars for the full page
    }
    return render(request, 'rotom/take_action.html', context)

def payment_success(request):
    tx_ref = request.GET.get('tx_ref')
    try:
        payment = Payment.objects.get(tx_ref=tx_ref)
        context = {'tx_ref': tx_ref, 'status': payment.status}
    except Payment.DoesNotExist:
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
    context = {}
    return render(request, 'rotom/champions.html', context)