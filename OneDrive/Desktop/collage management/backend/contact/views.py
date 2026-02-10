from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

from .models import ContactSubmission
from .serializers import ContactSubmissionSerializer
from authentication.services import send_email_notification, send_sms_notification

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_contact_form(request):
    """Submit contact form and send notifications"""
    serializer = ContactSubmissionSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save submission
        submission = serializer.save()
        
        # Prepare notification message
        email_message = f"""
New Contact Form Submission

Name: {submission.name}
Email: {submission.email}
Phone: {submission.phone}

Message:
{submission.message}

Submitted at: {submission.created_at.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        sms_message = f"New contact from {submission.name}. Email: {submission.email}, Phone: {submission.phone}"
        
        # Send email notification
        try:
            send_email_notification(
                to_email=settings.CONTACT_EMAIL,
                subject='New Contact Form Submission - AMIT',
                message=email_message
            )
            submission.email_sent = True
        except Exception as e:
            # Log but don't fail
            pass
        
        # Send SMS notifications
        sms_success = True
        try:
            send_sms_notification(settings.CONTACT_PHONE_1, sms_message)
            send_sms_notification(settings.CONTACT_PHONE_2, sms_message)
            submission.sms_sent = True
        except Exception as e:
            sms_success = False
        
        submission.save()
        
        return Response({
            'message': 'Contact form submitted successfully',
            'submission': ContactSubmissionSerializer(submission).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
