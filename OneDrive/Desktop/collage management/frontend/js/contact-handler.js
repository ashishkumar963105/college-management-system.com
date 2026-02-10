// Contact Form Handler

async function handleContactForm(formData) {
  const data = {
    name: formData.get('name'),
    email: formData.get('email'),
    phone: formData.get('phone'),
    message: formData.get('message')
  };
  
  // Validate data
  if (!data.name || !data.email || !data.phone || !data.message) {
    showError('❌ Please fill all fields');
    return { success: false, error: 'Missing fields' };
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}/contact/submit/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });
    
    const result = await response.json();
    
    if (response.ok) {
      showSuccess('✅ Message sent successfully! We will contact you soon.');
      return { success: true, data: result };
    } else {
      const errorMsg = result.error?.message || result.message || 'Failed to send message';
      showError('❌ Error: ' + errorMsg);
      return { success: false, error: errorMsg };
    }
  } catch (error) {
    showError('❌ Network error: ' + error.message);
    return { success: false, error: error.message };
  }
}

// Initialize contact form on page load
window.addEventListener('DOMContentLoaded', () => {
  const contactForm = document.getElementById('contactForm');
  
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const submitButton = contactForm.querySelector('button[type="submit"]');
      showLoading(submitButton);
      
      const formData = new FormData(contactForm);
      const result = await handleContactForm(formData);
      
      hideLoading(submitButton);
      
      if (result.success) {
        contactForm.reset();
      }
    });
    
    console.log('✅ Contact form handler initialized');
  }
});

console.log('✅ Contact handler module loaded');
