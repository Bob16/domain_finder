"""
Django app configuration for Domain Finder.
"""
from django.apps import AppConfig

class DomainFinderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'domain_finder'
    verbose_name = 'Domain Finder'