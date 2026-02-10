# College Management System Backend

Django REST API for Adwaita Mission Institute of Technology

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Set up Environment Variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Run Migrations**
```bash
python manage.py migrate
```

4. **Create Superuser**
```bash
python create_superuser.py
# Or manually: python manage.py createsuperuser
```

5. **Run Development Server**
```bash
python manage.py runserver
```

Server will start at: `http://localhost:8000`

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/logout/` - Logout user
- `POST /api/auth/forgot-password/` - Request password reset
- `POST /api/auth/reset-password/` - Reset password with token
- `GET /api/auth/verify-token/` - Verify JWT token
- `POST /api/auth/refresh-token/` - Refresh JWT token
- `POST /api/auth/setup/` - Complete first-time user setup

### Contact
- `POST /api/contact/submit/` - Submit contact form

### Admin Panel
- `/admin/` - Django admin panel

## 🔑 Default Credentials

**Admin Account:**
- Email: `admin@amit.edu`
- Password: `admin123`

## 📧 Email & SMS Configuration

### SendGrid (Email)
1. Sign up at https://sendgrid.com
2. Get API key
3. Add to `.env`:
```
SENDGRID_API_KEY=your_api_key_here
```

### Twilio (SMS)
1. Sign up at https://twilio.com
2. Get Account SID, Auth Token, and Phone Number
3. Add to `.env`:
```
TWILIO_ACCOUNT_SID=your_sid_here
TWILIO_AUTH_TOKEN=your_token_here
TWILIO_PHONE_NUMBER=your_twilio_number
```

## 🌐 Deployment

### Deploy to Render.com (FREE)

1. **Create Account** at https://render.com

2. **Create PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Name: `college_db`
   - Copy the "Internal Database URL"

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - Name: `amit-backend`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn college_system.wsgi:application`

4. **Add Environment Variables**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   DATABASE_URL=<paste-internal-database-url>
   ALLOWED_HOSTS=your-app-name.onrender.com
   SENDGRID_API_KEY=your-sendgrid-key
   TWILIO_ACCOUNT_SID=your-twilio-sid
   TWILIO_AUTH_TOKEN=your-twilio-token
   TWILIO_PHONE_NUMBER=your-twilio-number
   CONTACT_EMAIL=adwaitaaravind@gmail.com
   CONTACT_PHONE_1=+919801820820
   CONTACT_PHONE_2=+918920770080
   CORS_ALLOWED_ORIGINS=https://your-frontend-url.com
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

6. **Run Migrations**
   - Go to "Shell" tab
   - Run: `python manage.py migrate`
   - Run: `python create_superuser.py`

### Deploy to Railway (FREE)

1. **Create Account** at https://railway.app

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add PostgreSQL**
   - Click "New" → "Database" → "Add PostgreSQL"

4. **Configure Service**
   - Click on your service
   - Go to "Variables" tab
   - Add all environment variables (same as Render)

5. **Deploy**
   - Railway will auto-deploy
   - Get your public URL from "Settings" → "Domains"

## 🧪 Testing

### Test Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "Test@123",
    "password2": "Test@123",
    "name": "Test Student",
    "role": "student"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "Test@123"
  }'
```

### Test Contact Form
```bash
curl -X POST http://localhost:8000/api/contact/submit/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+919876543210",
    "message": "Test message"
  }'
```

## 📱 Frontend Integration

### JavaScript Example
```javascript
// Login
const response = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'student@test.com',
    password: 'Test@123'
  })
});

const data = await response.json();
const accessToken = data.tokens.access;

// Store token
localStorage.setItem('access_token', accessToken);

// Use token for authenticated requests
const profileResponse = await fetch('http://localhost:8000/api/auth/verify-token/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

## 🔒 Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT authentication
- ✅ CORS protection
- ✅ Input validation and sanitization
- ✅ Rate limiting on authentication
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection

## 📊 Database Models

- **User** - Base user model with email authentication
- **StudentProfile** - Student-specific information
- **FacultyProfile** - Faculty-specific information
- **AttendanceRecord** - Student attendance tracking
- **GradeRecord** - Student grades and marks
- **Announcement** - Faculty announcements
- **ContactSubmission** - Contact form submissions
- **NotificationLog** - Email/SMS notification logs
- **PasswordResetToken** - Password reset tokens

## 🛠️ Tech Stack

- **Framework:** Django 5.0.1
- **API:** Django REST Framework 3.14.0
- **Authentication:** JWT (djangorestframework-simplejwt)
- **Database:** PostgreSQL (production) / SQLite (development)
- **Email:** SendGrid
- **SMS:** Twilio
- **Deployment:** Render.com / Railway

## 📞 Support

For issues or questions:
- Email: adwaitaaravind@gmail.com
- Phone: +91-9801820820, +91-8920770080

## 📝 License

© 2024 Adwaita Mission Institute of Technology
