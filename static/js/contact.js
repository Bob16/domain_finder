// Contact form AJAX functionality - DEBUGGING VERSION

document.addEventListener('DOMContentLoaded', function() {
  console.log('=== CONTACT FORM DEBUG VERSION LOADED ===');
  
  // Add immediate debugging
  console.log('🔍 DOM Ready - checking for contact form...');
  console.log('🔍 All elements with ID:', document.querySelectorAll('[id]'));
  console.log('🔍 All forms:', document.querySelectorAll('form'));
  
  const contactForm = document.getElementById('contact-form');
  
  if (contactForm) {
    console.log('✅ Contact form found!', contactForm);
    console.log('✅ Form ID:', contactForm.id);
    console.log('✅ Form action:', contactForm.action);
    console.log('✅ Form method:', contactForm.method);
    
    // Add event listener with extra debugging
    contactForm.addEventListener('submit', function(e) {
      console.log('🎯 FORM SUBMIT EVENT TRIGGERED!!!');
      console.log('🎯 Event:', e);
      console.log('🎯 About to call handleContactSubmit...');
      handleContactSubmit(e);
    });
    
    console.log('✅ Event listener attached successfully');
    
    // Reset button functionality
    const resetButton = contactForm.querySelector('button[type="reset"]');
    if (resetButton) {
      resetButton.addEventListener('click', handleFormReset);
    }
  } else {
    console.error('❌ Contact form not found!');
    console.error('❌ Available elements with contact in ID or class:', 
      document.querySelectorAll('[id*="contact"], [class*="contact"]'));
  }
  
  // Test toast function to verify it works
  window.testToast = function() {
    console.log('🧪 Testing toast function...');
    showToast('✅ Toast system is working!', 'success');
  };
  console.log('🧪 You can test toasts by typing: testToast() in console');
  
  // Add a test alert to make sure this file is loaded
  console.log('🟢 JavaScript file fully loaded and executed!');
});

async function handleContactSubmit(e) {
  console.log('🚀 === FORM SUBMISSION STARTED ===');
  e.preventDefault();
  
  const form = e.target;
  const submitButton = form.querySelector('button[type="submit"]');
  const originalButtonText = submitButton.innerHTML;
  
  // Clear previous errors
  clearFormErrors();
  
  // Get form data
  const formData = new FormData(form);
  const data = {
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
    csrfmiddlewaretoken: formData.get('csrfmiddlewaretoken')
  };
  
  console.log('📝 Form data collected:', { 
    name: data.name, 
    email: data.email, 
    message: data.message ? data.message.substring(0, 50) + '...' : 'empty' 
  });
  
  // Basic client-side validation
  let hasErrors = false;
  
  if (!validateRequired(data.name)) {
    showFieldError('name', 'Name is required');
    hasErrors = true;
  } else if (data.name.length < 2) {
    showFieldError('name', 'Name must be at least 2 characters long');
    hasErrors = true;
  }
  
  if (!validateRequired(data.email)) {
    showFieldError('email', 'Email is required');
    hasErrors = true;
  } else if (!validateEmail(data.email)) {
    showFieldError('email', 'Please enter a valid email address');
    hasErrors = true;
  }
  
  if (!validateRequired(data.message)) {
    showFieldError('message', 'Message is required');
    hasErrors = true;
  } else if (data.message.length < 10) {
    showFieldError('message', 'Message must be at least 10 characters long');
    hasErrors = true;
  }
  
  if (hasErrors) {
    console.log('❌ Form validation failed, stopping submission');
    return;
  }
  
  console.log('✅ Form validation passed, proceeding with submission');
  
  // Show loading state
  submitButton.disabled = true;
  submitButton.innerHTML = `
    <svg class="animate-spin mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32">
        <animate attributeName="stroke-dasharray" dur="2s" values="0 64;32 32;0 64" repeatCount="indefinite" />
        <animate attributeName="stroke-dashoffset" dur="2s" values="0;-32;-64" repeatCount="indefinite" />
      </circle>
    </svg>
    Sending...
  `;

  try {
    console.log('🔒 Getting reCAPTCHA token...');
    
    // Get reCAPTCHA v3 token
    let recaptchaToken = null;
    if (typeof grecaptcha !== 'undefined') {
      try {
        recaptchaToken = await grecaptcha.execute('6LdBOdgrAAAAABo_6K1nkixlUykL2gdIbrSVWFPr', { action: 'submit' });
        data.captcha = recaptchaToken;
        console.log('✅ reCAPTCHA token obtained');
      } catch (recaptchaError) {
        console.error('❌ reCAPTCHA error:', recaptchaError);
        showToast('Security verification failed. Please try again.', 'error');
        // Re-enable submit button
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
        return;
      }
    } else {
      console.warn('⚠️ reCAPTCHA not loaded, proceeding without it');
    }

    console.log('📡 Sending AJAX request to /ajax/contact/');
    
    const response = await fetch('/ajax/contact/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': data.csrfmiddlewaretoken
      },
      body: JSON.stringify({
        name: data.name,
        email: data.email,
        message: data.message,
        captcha: data.captcha
      })
    });
    
    console.log('📡 Response received, status:', response.status);
    
    const result = await response.json();
    console.log('📦 RESPONSE DATA:', result);
    
    if (result.success) {
      showToast(result.message || 'Message sent successfully! We\'ll get back to you soon.', 'success');
      form.reset();
      clearFormErrors();
    } else {
      if (result.errors) {
        // Show server-side validation errors
        Object.keys(result.errors).forEach(field => {
          if (result.errors[field] && result.errors[field].length > 0) {
            showFieldError(field, result.errors[field][0]);
          }
        });
      } else {
        showToast(result.message || 'An error occurred. Please try again.', 'error');
      }
    }
  } catch (error) {
    console.error('💥 AJAX Error:', error);
    showToast('Network error. Please check your connection and try again.', 'error');
  } finally {
    console.log('🔄 Finally block: Restoring button state');
    // Restore button state
    submitButton.disabled = false;
    submitButton.innerHTML = originalButtonText;
    console.log('=== FORM SUBMISSION COMPLETED ===');
  }
}

function handleFormReset(e) {
  clearFormErrors();
  showToast('Form reset', 'info');
}

function showFieldError(fieldName, message) {
  const errorContainer = document.getElementById(`${fieldName}-errors`);
  const field = document.querySelector(`[name="${fieldName}"]`);
  
  if (errorContainer) {
    errorContainer.textContent = message;
    errorContainer.classList.remove('hidden');
  }
  
  if (field) {
    field.classList.add('border-red-500');
    field.classList.remove('border-input');
  }
}

function clearFormErrors() {
  const errorContainers = document.querySelectorAll('[id$="-errors"]');
  errorContainers.forEach(container => {
    container.classList.add('hidden');
    container.textContent = '';
  });
  
  const fields = document.querySelectorAll('[name="name"], [name="email"], [name="message"]');
  fields.forEach(field => {
    field.classList.remove('border-red-500');
    field.classList.add('border-input');
  });
}

function validateRequired(value) {
  return value && value.trim().length > 0;
}

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function showToast(message, type = 'info') {
  console.log('🍞 === INLINE TOAST FUNCTION CALLED ===');
  console.log('🍞 Message:', message);
  console.log('🍞 Type:', type);
  
  // Find the inline toast container
  const toastContainer = document.getElementById('contact-toast-container');
  const toastElement = document.getElementById('contact-toast');
  const toastMessage = document.getElementById('toast-message');
  const toastIcon = document.getElementById('toast-icon');
  
  if (!toastContainer || !toastElement || !toastMessage || !toastIcon) {
    console.error('❌ Toast elements not found!');
    console.error('Container:', toastContainer);
    console.error('Toast:', toastElement);
    console.error('Message:', toastMessage);
    console.error('Icon:', toastIcon);
    return;
  }
  
  console.log('✅ All toast elements found');
  
  // Set icon and styling based on type
  let icon, bgClass, textClass, borderClass;
  if (type === 'success') {
    icon = '✅';
    bgClass = 'bg-green-50';
    textClass = 'text-green-800';
    borderClass = 'border-green-200';
    console.log('🍞 Success styling applied');
  } else if (type === 'error') {
    icon = '❌';
    bgClass = 'bg-red-50';
    textClass = 'text-red-800';
    borderClass = 'border-red-200';
    console.log('🍞 Error styling applied');
  } else {
    icon = 'ℹ️';
    bgClass = 'bg-blue-50';
    textClass = 'text-blue-800';
    borderClass = 'border-blue-200';
    console.log('🍞 Info styling applied');
  }
  
  // Update toast content
  toastIcon.textContent = icon;
  toastMessage.textContent = message;
  
  // Reset classes and add new ones
  toastElement.className = `p-4 rounded-lg border shadow-sm transition-all duration-300 ease-in-out ${bgClass} ${textClass} ${borderClass}`;
  
  // Show the container
  toastContainer.classList.remove('hidden');
  
  // Reset animation classes
  toastElement.classList.remove('translate-y-[-10px]', 'opacity-0');
  toastElement.classList.add('translate-y-0', 'opacity-100');
  
  console.log('🍞 Toast shown with inline positioning');
  
  // Auto-hide after 5 seconds
  setTimeout(() => {
    if (!toastContainer.classList.contains('hidden')) {
      // Fade out animation
      toastElement.classList.remove('translate-y-0', 'opacity-100');
      toastElement.classList.add('translate-y-[-10px]', 'opacity-0');
      
      // Hide container after animation
      setTimeout(() => {
        toastContainer.classList.add('hidden');
        console.log('🍞 Toast hidden after auto-timeout');
      }, 300);
    }
  }, 5000);
  
  console.log('🍞 === INLINE TOAST FUNCTION COMPLETED ===');
}