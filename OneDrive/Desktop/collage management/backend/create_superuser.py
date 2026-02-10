import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_system.settings')
django.setup()

from users.models import User

# Create superuser
email = 'admin@amit.edu'
password = 'admin123'
name = 'Admin User'

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        password=password,
        name=name
    )
    print(f'Superuser created successfully!')
    print(f'Email: {email}')
    print(f'Password: {password}')
else:
    print('Superuser already exists')
