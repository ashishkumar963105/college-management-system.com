from django.contrib import admin
from .models import ContactSubmission, NotificationLog

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'email_sent', 'sms_sent', 'created_at')
    list_filter = ('status', 'email_sent', 'sms_sent', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('status', 'email_sent', 'sms_sent', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('type', 'recipient', 'status', 'retry_count', 'created_at')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('recipient', 'content')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
