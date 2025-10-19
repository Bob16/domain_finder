"""
URL configuration for the domain_finder app.
"""
from django.urls import path
from . import views

app_name = 'domain_finder'

urlpatterns = [
    path('', views.home, name='home'),
    path('domains/', views.domains_view, name='domains'),
    path('domains/load-more/', views.load_more_domains, name='load_more_domains'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('ajax/contact/', views.contact_ajax, name='contact_ajax'),
    # Test 404 page (works in development)
    path('test-404/', views.custom_404_view, name='test_404'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms-uk/', views.terms_uk, name='terms_uk'),
    path('complaints-appeals/', views.complaints_appeals, name='complaints_appeals'),
]