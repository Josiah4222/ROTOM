from django.core.management.base import BaseCommand
from django.conf import settings
from rotom.models import Payment
import requests
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Re-verify ALL payments with Chapa API to ensure correct status'

    def handle(self, *args, **options):
        all_payments = Payment.objects.all().order_by('-created_at')
        
        self.stdout.write(f"Found {all_payments.count()} total payments")
        self.stdout.write("=" * 70)
        
        success_count = 0
        failed_count = 0
        pending_count = 0
        error_count = 0
        corrected_count = 0
        
        for payment in all_payments:
            old_status = payment.status
            
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
                    success_count += 1
                    if old_status != 'success':
                        corrected_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'✓ CORRECTED: {payment.tx_ref} ({old_status} → success)')
                        )
                    else:
                        self.stdout.write(f'  {payment.tx_ref}: success (unchanged)')
                        
                elif 'failed' in chapa_status or 'cancel' in chapa_status:
                    # Handles: 'failed', 'cancelled', 'canceled', 'failed/cancelled', etc.
                    payment.status = 'failed'
                    payment.save()
                    failed_count += 1
                    if old_status != 'failed':
                        corrected_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'✗ CORRECTED: {payment.tx_ref} ({old_status} → failed) [Chapa: {chapa_status}]')
                        )
                    else:
                        self.stdout.write(f'  {payment.tx_ref}: failed (unchanged)')
                        
                else:
                    # Keep or set as pending
                    if payment.status != 'pending':
                        old_status_display = payment.status
                        payment.status = 'pending'
                        payment.save()
                        corrected_count += 1
                        self.stdout.write(
                            self.style.WARNING(f'⏳ CORRECTED: {payment.tx_ref} ({old_status_display} → pending) [Chapa: {chapa_status}]')
                        )
                    else:
                        self.stdout.write(f'  {payment.tx_ref}: pending (unchanged) [Chapa: {chapa_status}]')
                    pending_count += 1
                        
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'❌ ERROR verifying {payment.tx_ref}: {str(e)}')
                )
        
        self.stdout.write("")
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("\nVerification Summary:"))
        self.stdout.write(f"  Total payments checked: {all_payments.count()}")
        self.stdout.write(f"  ✓ Success: {success_count}")
        self.stdout.write(f"  ✗ Failed: {failed_count}")
        self.stdout.write(f"  ⏳ Pending: {pending_count}")
        self.stdout.write(f"  ❌ Errors: {error_count}")
        self.stdout.write(f"  🔄 Corrected: {corrected_count}")
