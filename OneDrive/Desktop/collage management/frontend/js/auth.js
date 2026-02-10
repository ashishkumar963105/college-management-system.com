// Authentication handlers

// Handle Registration
async function handleRegistration(formData) {
  const data = {
    email: formData.get('email'),
    password: formData.get('password'),
    password2: formData.get('password2') || formData.get('password'),
    name: formData.get('name'),
    role: formData.get('role') || 'student'
  };
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });
    
    const result = await response.json();
    
    if (response.ok) {
      showSuccess('✅ Registration successful! Please login.');
      return { success: true, data: result };
    } else {
      const errorMsg = result.error?.message || result.message || JSON.stringify(result);
      showError('❌ Registration failed: ' + errorMsg);
      return { success: false, error: errorMsg };
    }
  } catch (error) {
    showError('❌ Network error: ' + error.message);
    return { success: false, error: error.message };
  }
}

// Handle Login
async function handleLogin(email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password })
    });
    
    const result = await response.json();
    
    if (response.ok) {
      // Store tokens and user data
      localStorage.setItem('access_token', result.tokens.access);
      localStorage.setItem('refresh_token', result.tokens.refresh);
      localStorage.setItem('user', JSON.stringify(result.user));
      
      showSuccess('✅ Login successful!');
      
      // Redirect based on role
      setTimeout(() => {
        if (result.user.role === 'student') {
          window.location.href = 'student-portal.html';
        } else if (result.user.role === 'faculty') {
          window.location.href = 'faculty-portal.html';
        } else if (result.user.role === 'admin') {
          window.location.href = 'http://localhost:8000/admin/';
        }
      }, 500);
      
      return { success: true, data: result };
    } else {
      const errorMsg = result.error?.message || result.message || 'Invalid credentials';
      showError('❌ Login failed: ' + errorMsg);
      return { success: false, error: errorMsg };
    }
  } catch (error) {
    showError('❌ Network error: ' + error.message);
    return { success: false, error: error.message };
  }
}

// Handle Forgot Password
async function handleForgotPassword(email) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/forgot-password/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email })
    });
    
    const result = await response.json();
    
    if (response.ok) {
      showSuccess('✅ Password reset email sent! Check your inbox.');
      return { success: true, data: result };
    } else {
      const errorMsg = result.error?.message || result.message || 'Failed to send reset email';
      showError('❌ Error: ' + errorMsg);
      return { success: false, error: errorMsg };
    }
  } catch (error) {
    showError('❌ Network error: ' + error.message);
    return { success: false, error: error.message };
  }
}

// Check authentication on protected pages
function checkAuthentication(requiredRole = null) {
  if (!isAuthenticated()) {
    window.location.href = 'index.html';
    return false;
  }
  
  const user = getCurrentUser();
  
  if (requiredRole && user.role !== requiredRole) {
    alert('Access denied. You do not have permission to view this page.');
    window.location.href = 'index.html';
    return false;
  }
  
  return true;
}

// Verify token on page load
async function verifyToken() {
  const token = localStorage.getItem('access_token');
  
  if (!token) {
    return false;
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/verify-token/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) {
      // Token expired or invalid
      localStorage.clear();
      return false;
    }
    
    return true;
  } catch (error) {
    console.error('Token verification failed:', error);
    return false;
  }
}

// Initialize authentication on page load
window.addEventListener('DOMContentLoaded', () => {
  // Check if we're on a protected page
  const protectedPages = ['student-portal.html', 'faculty-portal.html'];
  const currentPage = window.location.pathname.split('/').pop();
  
  if (protectedPages.includes(currentPage)) {
    verifyToken().then(valid => {
      if (!valid) {
        window.location.href = 'index.html';
      }
    });
  }
});

console.log('✅ Auth module loaded successfully');
