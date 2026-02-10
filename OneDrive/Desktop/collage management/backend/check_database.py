import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_system.settings')
django.setup()

from users.models import User, StudentProfile, FacultyProfile
from contact.models import ContactSubmission, NotificationLog

print("\n" + "="*60)
print("DATABASE STATUS CHECK")
print("="*60)

# Check Users
users = User.objects.all()
print(f"\n✅ Total Users: {users.count()}")
for user in users:
    print(f"   - {user.name} ({user.email}) - Role: {user.role}")

# Check Students
students = StudentProfile.objects.all()
print(f"\n✅ Total Students: {students.count()}")
for student in students:
    print(f"   - {student.user.name} (ID: {student.student_id})")

# Check Faculty
faculty = FacultyProfile.objects.all()
print(f"\n✅ Total Faculty: {faculty.count()}")
for fac in faculty:
    print(f"   - {fac.user.name} (ID: {fac.faculty_id})")

# Check Contact Submissions
contacts = ContactSubmission.objects.all()
print(f"\n✅ Total Contact Submissions: {contacts.count()}")
for contact in contacts[:5]:  # Show last 5
    print(f"   - {contact.name} ({contact.email}) - {contact.created_at.strftime('%Y-%m-%d %H:%M')}")

# Check Notifications
notifications = NotificationLog.objects.all()
print(f"\n✅ Total Notifications: {notifications.count()}")
print(f"   - Email: {NotificationLog.objects.filter(type='email').count()}")
print(f"   - SMS: {NotificationLog.objects.filter(type='sms').count()}")

print("\n" + "="*60)
print("DATABASE IS CONNECTED AND WORKING! ✅")
print("="*60 + "\n")
