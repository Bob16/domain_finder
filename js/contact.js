// Contact form AJAX functionality

document.addEventListener('DOMContentLoaded', function() {
  const contactForm = document.getElementById('contact-form');
  
  if (contactForm) {
    contactForm.addEventListener('submit', handleContactSubmit);
    
    // Reset button functionality
    const resetButton = contactForm.querySelector('button[type="reset"]');
    if (resetButton) {
      resetButton.addEventListener('click', handleFormReset);
    }
  }
});

async function handleContactSubmit(e) {
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
    return;
  }
  
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
    const response = await fetch('/ajax/contact/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': data.csrfmiddlewaretoken
      },
      body: JSON.stringify({
        name: data.name,
        email: data.email,
        message: data.message
      })
    });
    
    const result = await response.json();
    
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
    console.error('Error submitting contact form:', error);
    showToast('Network error. Please check your connection and try again.', 'error');
  } finally {
    // Restore button state
    submitButton.disabled = false;
    submitButton.innerHTML = originalButtonText;
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