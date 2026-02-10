"""
Complete test of ALL functions - Registration, Login, Contact Form
This will verify everything is saving to database
"""
import os
import django
import requests
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_system.settings')
django.setup()

from users.models import User, StudentProfile
from contact.models import ContactSubmission, NotificationLog

API_URL = 'http://localhost:8000/api'

print("\n" + "="*70)
print("COMPLETE FUNCTION TEST - ALL FEATURES")
print("="*70)

# Test email with timestamp
test_email = f'testuser{int(datetime.now().timestamp())}@student.com'
test_password = 'Test@123456'

# ============================================================================
# TEST 1: REGISTRATION
# ============================================================================
print("\n" + "-"*70)
print("TEST 1: REGISTRATION")
print("-"*70)

print("\n📝 Sending registration request...")
reg_data = {
    'email': test_email,
    'password': test_password,
    'password2': test_password,
    'name': 'Complete Test Student',
    'role': 'student'
}

try:
    response = requests.post(f'{API_URL}/auth/register/', json=reg_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ Registration API: SUCCESS")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        # Verify in database
        try:
            user = User.objects.get(email=test_email)
            print(f"\n✅ DATABASE CHECK: User found!")
            print(f"   - Name: {user.name}")
            print(f"   - Email: {user.email}")
            print(f"   - Role: {user.role}")
            print(f"   - Active: {user.is_active}")
            print(f"   - Created: {user.created_at}")
        except User.DoesNotExist:
            print("❌ DATABASE CHECK: User NOT found in database!")
            print("⚠️ REGISTRATION NOT SAVING TO DATABASE!")
    else:
        print(f"❌ Registration API: FAILED")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Registration Error: {str(e)}")

# ============================================================================
# TEST 2: LOGIN
# ============================================================================
print("\n" + "-"*70)
print("TEST 2: LOGIN")
print("-"*70)

print("\n🔐 Sending login request...")
login_data = {
    'email': test_email,
    'password': test_password
}

try:
    response = requests.post(f'{API_URL}/auth/login/', json=login_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Login API: SUCCESS")
        data = response.json()
        print(f"✅ Got JWT Token: {data['tokens']['access'][:50]}...")
        
        # Verify last_login updated in database
        user = User.objects.get(email=test_email)
        if user.last_login:
            print(f"\n✅ DATABASE CHECK: Last login updated!")
            print(f"   - Last Login: {user.last_login}")
        else:
            print("❌ DATABASE CHECK: Last login NOT updated!")
    else:
        print(f"❌ Login API: FAILED")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Login Error: {str(e)}")

# ============================================================================
# TEST 3: CONTACT FORM
# ============================================================================
print("\n" + "-"*70)
print("TEST 3: CONTACT FORM")
print("-"*70)

print("\n📧 Sending contact form...")
contact_data = {
    'name': 'Test Contact User',
    'email': 'testcontact@example.com',
    'phone': '+919876543210',
    'message': 'This is a complete test of contact form functionality'
}

try:
    response = requests.post(f'{API_URL}/contact/submit/', json=contact_data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ Contact Form API: SUCCESS")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        
        # Verify in database
        try:
            contact = ContactSubmission.objects.get(email='testcontact@example.com')
            print(f"\n✅ DATABASE CHECK: Contact submission found!")
            print(f"   - Name: {contact.name}")
            print(f"   - Email: {contact.email}")
            print(f"   - Phone: {contact.phone}")
            print(f"   - Message: {contact.message[:50]}...")
            print(f"   - Status: {contact.status}")
            print(f"   - Created: {contact.created_at}")
        except ContactSubmission.DoesNotExist:
            print("❌ DATABASE CHECK: Contact submission NOT found!")
            print("⚠️ CONTACT FORM NOT SAVING TO DATABASE!")
    else:
        print(f"❌ Contact Form API: FAILED")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Contact Form Error: {str(e)}")

# ============================================================================
# FINAL DATABASE SUMMARY
# ============================================================================
print("\n" + "="*70)
print("FINAL DATABASE SUMMARY")
print("="*70)

total_users = User.objects.count()
total_contacts = ContactSubmission.objects.count()
total_notifications = NotificationLog.objects.count()

print(f"\n📊 Database Statistics:")
print(f"   - Total Users: {total_users}")
print(f"   - Total Contact Submissions: {total_contacts}")
print(f"   - Total Notification Logs: {total_notifications}")

print("\n👥 All Users:")
for user in User.objects.all():
    print(f"   - {user.name} ({user.email}) - {user.role}")

print("\n📧 Recent Contact Submissions:")
for contact in ContactSubmission.objects.all().order_by('-created_at')[:5]:
    print(f"   - {contact.name} ({contact.email}) - {contact.created_at.strftime('%Y-%m-%d %H:%M')}")

# ============================================================================
# FINAL VERDICT
# ============================================================================
print("\n" + "="*70)
print("FINAL VERDICT")
print("="*70)

all_working = True
issues = []

# Check if new user was created
if User.objects.filter(email=test_email).exists():
    print("✅ Registration: WORKING - Data saved to database")
else:
    print("❌ Registration: NOT WORKING - Data not saved")
    all_working = False
    issues.append("Registration not saving to database")

# Check if contact was created
if ContactSubmission.objects.filter(email='testcontact@example.com').exists():
    print("✅ Contact Form: WORKING - Data saved to database")
else:
    print("❌ Contact Form: NOT WORKING - Data not saved")
    all_working = False
    issues.append("Contact form not saving to database")

# Check if login updated last_login
user = User.objects.get(email=test_email)
if user.last_login:
    print("✅ Login: WORKING - Last login updated")
else:
    print("❌ Login: NOT WORKING - Last login not updated")
    all_working = False
    issues.append("Login not updating last_login")

print("\n" + "="*70)
if all_working:
    print("🎉 ALL FUNCTIONS WORKING PERFECTLY!")
    print("✅ Everything is saving to database correctly!")
    print("✅ System is 100% ready for demo!")
else:
    print("⚠️ SOME ISSUES FOUND:")
    for issue in issues:
        print(f"   - {issue}")
    print("\n❌ SYSTEM NEEDS FIXES!")
print("="*70 + "\n")
