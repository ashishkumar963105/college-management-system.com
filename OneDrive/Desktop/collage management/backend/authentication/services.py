from django.core.mail import send_mail
from django.conf import settings
from contact.models import NotificationLog
import time

def send_email_notification(to_email, subject, message, html_message=None, max_retries=3):
    """Send email with retry logic"""
    for attempt in range(max_retries):
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[to_email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Log success
            NotificationLog.objects.create(
                type='email',
                recipient=to_email,
                content=f"{subject}: {message[:100]}",
                status='success',
                retry_count=attempt
            )
            return True
            
        except Exception as e:
            if attempt == max_retries - 1:
                # Log final failure
                NotificationLog.objects.create(
                    type='email',
                    recipient=to_email,
                    content=f"{subject}: {message[:100]}",
                    status='failed',
                    error_message=str(e),
                    retry_count=attempt + 1
                )
                raise
            # Exponential backoff
            time.sleep(2 ** attempt)
    
    return False

def send_sms_notification(to_phone, message, max_retries=3):
    """Send SMS with retry logic using Twilio"""
    from twilio.rest import Client
    
    # Check if Twilio is configured
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        NotificationLog.objects.create(
            type='sms',
            recipient=to_phone,
            content=message[:100],
            status='failed',
            error_message='Twilio not configured'
        )
        return False
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    for attempt in range(max_retries):
        try:
            # Limit message to 160 characters
            if len(message) > 160:
                message = message[:157] + '...'
            
            client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=to_phone
            )
            
            # Log success
            NotificationLog.objects.create(
                type='sms',
                recipient=to_phone,
                content=message,
                status='success',
                retry_count=attempt
            )
            return True
            
        except Exception as e:
            if attempt == max_retries - 1:
                # Log final failure
                NotificationLog.objects.create(
                    type='sms',
                    recipient=to_phone,
                    content=message,
                    status='failed',
                    error_message=str(e),
                    retry_count=attempt + 1
                )
                return False
            # Exponential backoff
            time.sleep(2 ** attempt)
    
    return False
