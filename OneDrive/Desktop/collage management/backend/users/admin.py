from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, FacultyProfile, AttendanceRecord, GradeRecord, Announcement, PasswordResetToken

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'role', 'is_active', 'is_setup_complete', 'created_at')
    list_filter = ('role', 'is_active', 'is_setup_complete')
    search_fields = ('email', 'name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role')}),
        ('Status', {'fields': ('is_active', 'is_setup_complete', 'is_staff', 'is_superuser')}),
        ('Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password1', 'password2'),
        }),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'program', 'current_semester', 'enrollment_date')
    list_filter = ('program', 'current_semester')
    search_fields = ('student_id', 'user__name', 'user__email')
    ordering = ('-enrollment_date',)

@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('faculty_id', 'user', 'department', 'designation')
    list_filter = ('department', 'designation')
    search_fields = ('faculty_id', 'user__name', 'user__email', 'department')

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'status', 'faculty', 'marked_at')
    list_filter = ('status', 'date', 'subject')
    search_fields = ('student__student_id', 'student__user__name', 'subject')
    date_hierarchy = 'date'
    ordering = ('-date',)

@admin.register(GradeRecord)
class GradeRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'assessment_type', 'marks_obtained', 'total_marks', 'semester', 'faculty')
    list_filter = ('semester', 'assessment_type', 'subject')
    search_fields = ('student__student_id', 'student__user__name', 'subject')
    ordering = ('-created_at',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'faculty', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content', 'faculty__user__name')
    ordering = ('-created_at',)

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'used', 'expires_at', 'created_at')
    list_filter = ('used', 'expires_at')
    search_fields = ('user__email', 'token')
    ordering = ('-created_at',)
