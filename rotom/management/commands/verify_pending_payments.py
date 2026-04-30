from django.core.management.base import BaseCommand
from django.conf import settings
from rotom.models import Payment
import requests
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Verify pending payments with Chapa API'

    def handle(self, *args, **options):
        pending_payments = Payment.objects.filter(status='pending')
        
        self.stdout.write(f"Found {pending_payments.count()} pending payments")
        
        verified_count = 0
        failed_count = 0
        still_pending = 0
        
        for payment in pending_payments:
            try:
                url = f'https://api.chapa.co/v1/transaction/verify/{payment.tx_ref}'
                headers = {'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'}
                response = requests.get(url, headers=headers)
                response_data = response.json()
                
                # Check the actual transaction status from Chapa
                chapa_status = response_data.get('data', {}).get('status', '').lower()
                
                if chapa_status == 'success':
                    payment.status = 'success'
                    payment.save()
                    verified_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Payment {payment.tx_ref} verified as SUCCESS')
                    )
                elif 'failed' in chapa_status or 'cancel' in chapa_status:
                    # Handles: 'failed', 'cancelled', 'canceled', 'failed/cancelled', etc.
                    payment.status = 'failed'
                    payment.save()
                    failed_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'✗ Payment {payment.tx_ref} marked as FAILED (Chapa status: {chapa_status})')
                    )
                else:
                    still_pending += 1
                    self.stdout.write(
                        self.style.WARNING(f'- Payment {payment.tx_ref} still PENDING (Chapa status: {chapa_status})')
                    )
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error verifying {payment.tx_ref}: {str(e)}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nVerification complete: {verified_count} verified as success, {failed_count} failed, {still_pending} still pending'
            )
        )
