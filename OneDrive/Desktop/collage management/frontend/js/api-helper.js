// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Helper function for authenticated requests
async function authenticatedFetch(url, options = {}) {
  const token = localStorage.getItem('access_token');
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }
  };
  
  const mergedOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers
    }
  };
  
  try {
    const response = await fetch(url, mergedOptions);
    
    // Handle token expiration
    if (response.status === 401) {
      // Try to refresh token
      const refreshed = await refreshAccessToken();
      if (refreshed) {
        // Retry request with new token
        mergedOptions.headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`;
        return await fetch(url, mergedOptions);
      } else {
        // Refresh failed, redirect to login
        localStorage.clear();
        window.location.href = 'index.html';
        return null;
      }
    }
    
    return response;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

// Refresh access token
async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  
  if (!refreshToken) return false;
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/refresh-token/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken })
    });
    
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access);
      return true;
    }
    return false;
  } catch (error) {
    console.error('Token refresh error:', error);
    return false;
  }
}

// Check if user is authenticated
function isAuthenticated() {
  return !!localStorage.getItem('access_token');
}

// Get current user
function getCurrentUser() {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
}

// Logout function
async function logout() {
  const refreshToken = localStorage.getItem('refresh_token');
  const accessToken = localStorage.getItem('access_token');
  
  try {
    await fetch(`${API_BASE_URL}/auth/logout/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify({ refresh_token: refreshToken })
    });
  } catch (error) {
    console.error('Logout error:', error);
  }
  
  // Clear local storage
  localStorage.clear();
  window.location.href = 'index.html';
}

// Show loading indicator
function showLoading(button) {
  if (button) {
    button.disabled = true;
    button.dataset.originalText = button.textContent;
    button.textContent = 'Loading...';
  }
}

// Hide loading indicator
function hideLoading(button) {
  if (button) {
    button.disabled = false;
    button.textContent = button.dataset.originalText || button.textContent;
  }
}

// Display error message
function showError(message, elementId = null) {
  if (elementId) {
    const element = document.getElementById(elementId);
    if (element) {
      element.textContent = message;
      element.style.display = 'block';
      setTimeout(() => {
        element.style.display = 'none';
      }, 5000);
    }
  } else {
    alert(message);
  }
}

// Display success message
function showSuccess(message, elementId = null) {
  if (elementId) {
    const element = document.getElementById(elementId);
    if (element) {
      element.textContent = message;
      element.style.display = 'block';
      setTimeout(() => {
        element.style.display = 'none';
      }, 5000);
    }
  } else {
    alert(message);
  }
}

console.log('✅ API Helper loaded successfully');
console.log('🔗 API Base URL:', API_BASE_URL);
