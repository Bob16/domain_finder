"""
Django forms for the Domain Finder application.
"""
from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from .models import ContactSubmission

class ContactForm(forms.ModelForm):
    """Contact form with reCAPTCHA v3 validation."""
    
    # Add reCAPTCHA v3 field (invisible)
    captcha = ReCaptchaField(
        widget=ReCaptchaV3(action='submit'),
        label=""  # No label needed for v3 as it's invisible
    )
    
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'flex h-10 w-full rounded-md border border-input bg-input-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
                'placeholder': 'Your Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'flex h-10 w-full rounded-md border border-input bg-input-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
                'placeholder': 'your@email.com',
                'required': True,
            }),
            'message': forms.Textarea(attrs={
                'class': 'flex min-h-[80px] w-full rounded-md border border-input bg-input-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
                'placeholder': 'Tell us about your domain research needs...',
                'rows': 5,
                'required': True,
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        return message