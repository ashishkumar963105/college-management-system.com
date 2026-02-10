# 🎨 Frontend - College Management System

HTML/CSS/JavaScript frontend for Adwaita Mission Institute of Technology.

---

## 📁 Files

### Main Pages
- `index.html` - Home page
- `about.html` - About college
- `academics.html` - Academic programs
- `admissions.html` - Admission information
- `faculty.html` - Faculty listing
- `contact.html` - Contact form (API integrated)
- `library.html` - Library information
- `events.html` - College events

### Portal Pages
- `student-portal.html` - Student login & dashboard (API integrated)
- `faculty-portal.html` - Faculty login (API integrated)
- `first-time-user.html` - Student registration (API integrated)
- `forgot-password.html` - Password reset

### Syllabus Pages
- `syllabus-btech-cse.html` - B.Tech CSE
- `syllabus-btech-ece.html` - B.Tech ECE
- `syllabus-btech-mechanical.html` - B.Tech Mechanical
- `syllabus-btech-electrical.html` - B.Tech Electrical
- `syllabus-btech-civil.html` - B.Tech Civil
- `syllabus-bca.html` - BCA
- `syllabus-bba.html` - BBA

### Test & Setup
- `test-integration.html` - API integration test page
- `setup-images.html` - Image setup utility

---

## 📂 Folders

### `js/` - JavaScript Files
- `script.js` - Main scripts
- `portal.js` - Portal functionality
- `faculty.js` - Faculty page scripts
- `academics.js` - Academics page scripts
- `api-helper.js` - **API integration helper**
- `auth.js` - **Authentication handlers**
- `contact-handler.js` - **Contact form handler**

### `images/` - Images
- College photos
- Faculty photos
- Event photos
- Building photos

---

## 🔗 API Integration

### Connected Pages
1. **Contact Form** (`contact.html`)
   - Submits to: `/api/contact/submit/`
   - Shows success/error messages
   - Sends email + SMS notifications

2. **Student Registration** (`first-time-user.html`)
   - Submits to: `/api/auth/register/`
   - Creates user account
   - Auto-redirects to login

3. **Student Login** (`student-portal.html`)
   - Submits to: `/api/auth/login/`
   - Gets JWT token
   - Shows dashboard

4. **Faculty Login** (`faculty-portal.html`)
   - Submits to: `/api/auth/login/`
   - Role-based access
   - JWT authentication

---

## 🚀 How to Use

### 1. Start Backend First
```bash
cd ../backend
python manage.py runserver
```

### 2. Open Frontend
- Double-click any HTML file, OR
- Use Live Server in VS Code, OR
- Open with browser directly

### 3. Test Integration
- Open `test-integration.html`
- Click "Run All Tests"
- All should pass ✅

---

## 🎨 Styling

- `styles.css` - Main stylesheet
- `portal.css` - Portal-specific styles
- Responsive design
- Mobile-friendly
- Modern UI

---

## 🔧 Configuration

### API Base URL
Located in `js/api-helper.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

Change this for production deployment.

---

## ✅ Features

- ✅ Responsive design
- ✅ API integration
- ✅ Form validation
- ✅ Token management
- ✅ Error handling
- ✅ Loading indicators
- ✅ Success messages
- ✅ SEO optimized

---

## 📞 Support

Email: adwaitaaravind@gmail.com
Phone: +91-9801820820, +91-8920770080
