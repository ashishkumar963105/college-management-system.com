from rest_framework import serializers
from .models import ContactSubmission
import re

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ('id', 'name', 'email', 'phone', 'message', 'status', 'created_at')
        read_only_fields = ('id', 'status', 'created_at')
    
    def validate_email(self, value):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError('Invalid email format')
        return value
    
    def validate_phone(self, value):
        """Validate phone number format"""
        # Remove spaces and dashes
        phone = value.replace(' ', '').replace('-', '')
        # Check if it's a valid phone number (10-15 digits, may start with +)
        phone_regex = r'^\+?[0-9]{10,15}$'
        if not re.match(phone_regex, phone):
            raise serializers.ValidationError('Invalid phone number format')
        return value
