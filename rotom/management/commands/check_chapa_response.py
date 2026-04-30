from django.core.management.base import BaseCommand
from django.conf import settings
from rotom.models import Payment
import requests
import json


class Command(BaseCommand):
    help = 'Check Chapa API response for a specific transaction'

    def add_arguments(self, parser):
        parser.add_argument('tx_ref', type=str, help='Transaction reference to check')

    def handle(self, *args, **options):
        tx_ref = options['tx_ref']
        
        try:
            payment = Payment.objects.get(tx_ref=tx_ref)
            self.stdout.write(f"Found payment in database:")
            self.stdout.write(f"  TX Ref: {payment.tx_ref}")
            self.stdout.write(f"  Amount: {payment.amount} ETB")
            self.stdout.write(f"  Status: {payment.status}")
            self.stdout.write(f"  Email: {payment.email}")
            self.stdout.write(f"  Name: {payment.first_name} {payment.last_name}")
            self.stdout.write("")
        except Payment.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Payment not found in database: {tx_ref}"))
            return
        
        try:
            url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
            headers = {'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'}
            
            self.stdout.write(f"Calling Chapa API: {url}")
            response = requests.get(url, headers=headers)
            response_data = response.json()
            
            self.stdout.write(self.style.SUCCESS("\nChapa API Response:"))
            self.stdout.write(json.dumps(response_data, indent=2))
            
            # Extract key information
            if 'data' in response_data:
                data = response_data['data']
                self.stdout.write(self.style.SUCCESS("\n\nKey Information:"))
                self.stdout.write(f"  Status: {data.get('status', 'N/A')}")
                self.stdout.write(f"  Amount: {data.get('amount', 'N/A')}")
                self.stdout.write(f"  Currency: {data.get('currency', 'N/A')}")
                self.stdout.write(f"  Created At: {data.get('created_at', 'N/A')}")
                self.stdout.write(f"  Updated At: {data.get('updated_at', 'N/A')}")
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\nError calling Chapa API: {str(e)}"))
