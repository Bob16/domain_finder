"""
Context processors for Domain Finder.
"""
from .models import ContactInfo


def contact_info(request):
    """
    Make contact information available in all templates.
    """
    return {
        'contact_info': ContactInfo.get_active_contact_info()
    }