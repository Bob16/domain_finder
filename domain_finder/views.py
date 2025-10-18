"""
Django views for the Domain Finder application.
"""
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, get_connection
from django.contrib import messages
from django.conf import settings
from django.db import models
from .models import BlogPost, BlogCategory, ContactInfo, Domain, DomainStatus, Currency
from .forms import ContactForm

def home(request):
    """Home page view."""
    from .models import HomePage
    
    # Get featured blog post for hero section
    featured_post = BlogPost.objects.filter(is_featured=True, is_published=True).first()
    
    # Get active homepage content from database
    homepage_content = HomePage.objects.filter(is_active=True).first()
    
    # Fallback content if no active homepage content exists
    hero_content = {
        'title': "Find the Perfect <span class='text-primary'>Domain</span> for Your Business",
        'subtitle': "Our expert market research helps you discover high-value domains that align with your brand and business goals. Make informed decisions with data-driven insights.",
        'image': None
    }
    
    # Fallback statistics if no active homepage content exists
    statistics = {
        'domains_analyzed': '500+',
        'domains_analyzed_label': 'Domains Analyzed',
        'client_satisfaction': '98%',
        'client_satisfaction_label': 'Client Satisfaction',
        'response_time': '24h',
        'response_time_label': 'Avg. Response Time',
    }
    
    # Fallback Market Intelligence content
    market_intelligence = {
        'pill_text': 'Market Intelligence',
        'title': 'Data-Driven Domain Research',
        'subtitle': 'Our comprehensive analytics provide deep insights into domain performance, market trends, and competitive landscape.',
        'card1': {
            'title': 'Market Trends',
            'subtitle': 'Real-time analysis of domain market trends and pricing patterns',
            'number': '94%',
            'label': 'Accuracy Rate'
        },
        'card2': {
            'title': 'Brand Alignment',
            'subtitle': 'Evaluate how well domains match your brand identity and goals',
            'number': '89%',
            'label': 'Match Score'
        },
        'card3': {
            'title': 'Risk Assessment',
            'subtitle': 'Comprehensive domain history and legal risk evaluation',
            'number': '99%',
            'label': 'Clean Domains'
        }
    }
    
    # Use database content if available
    if homepage_content:
        hero_content = {
            'title': homepage_content.title,
            'subtitle': homepage_content.subtitle,
            'image': homepage_content.hero_image.url if homepage_content.hero_image else None,
        }
        statistics = {
            'domains_analyzed': homepage_content.domains_analyzed,
            'domains_analyzed_label': homepage_content.domains_analyzed_label,
            'client_satisfaction': homepage_content.client_satisfaction,
            'client_satisfaction_label': homepage_content.client_satisfaction_label,
            'response_time': homepage_content.response_time,
            'response_time_label': homepage_content.response_time_label,
        }
        market_intelligence = {
            'pill_text': homepage_content.market_intelligence_pill,
            'title': homepage_content.market_intelligence_title,
            'subtitle': homepage_content.market_intelligence_subtitle,
            'card1': {
                'title': homepage_content.card1_title,
                'subtitle': homepage_content.card1_subtitle,
                'number': homepage_content.card1_number,
                'label': homepage_content.card1_label
            },
            'card2': {
                'title': homepage_content.card2_title,
                'subtitle': homepage_content.card2_subtitle,
                'number': homepage_content.card2_number,
                'label': homepage_content.card2_label
            },
            'card3': {
                'title': homepage_content.card3_title,
                'subtitle': homepage_content.card3_subtitle,
                'number': homepage_content.card3_number,
                'label': homepage_content.card3_label
            }
        }
    
    # Advanced Analytics section toggle (default False)
    show_advanced_analytics = False
    if homepage_content:
        show_advanced_analytics = homepage_content.show_advanced_analytics
    
    context = {
        'page_title': 'Domain Finder - Expert Domain Research & Analytics',
        'featured_post': featured_post,
        'hero': hero_content,
        'stats': statistics,
        'market_intel': market_intelligence,
        'show_advanced_analytics': show_advanced_analytics,
    }
    return render(request, 'domain_finder/home.html', context)

def blog_list(request):
    """Blog listing page view."""
    category_slug = request.GET.get('category')
    
    # Get all published posts
    posts = BlogPost.objects.filter(is_published=True)
    
    # Filter by category if specified
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Get total count of posts (including featured)
    total_posts_count = posts.count()
    
    # Get featured post (separate from main list)
    featured_post = posts.filter(is_featured=True).first()
    
    # Get remaining posts (excluding featured if it exists)
    if featured_post:
        posts = posts.exclude(pk=featured_post.pk)
    
    # Get all categories for filter
    categories = BlogCategory.objects.all()
    
    # Check if we should show "Load More" button (more than 7 total articles)
    show_load_more = total_posts_count > 7
    
    context = {
        'page_title': 'Domain Research Blog - Expert Insights & Trends',
        'featured_post': featured_post,
        'posts': posts,
        'categories': categories,
        'current_category': category_slug,
        'total_posts_count': total_posts_count,
        'show_load_more': show_load_more,
    }
    return render(request, 'domain_finder/blog_list.html', context)

def blog_detail(request, post_id):
    """Blog post detail view."""
    post = get_object_or_404(BlogPost, pk=post_id, is_published=True)
    
    # Get related posts (same category, excluding current post)
    related_posts = BlogPost.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(pk=post.pk)[:2]
    
    context = {
        'page_title': f'{post.title} - Domain Finder Blog',
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'domain_finder/blog_detail.html', context)

def contact(request):
    """Contact page view."""
    form = ContactForm()
    
    context = {
        'page_title': 'Contact Us - Domain Finder',
        'form': form,
    }
    return render(request, 'domain_finder/contact.html', context)

@require_http_methods(["POST"])
def contact_ajax(request):
    """AJAX contact form submission."""
    try:
        # Parse JSON data
        data = json.loads(request.body)
        
        # Create form instance with data
        form = ContactForm(data)
        
        if form.is_valid():
            # Save the contact submission
            contact_submission = form.save()
            
            # Get SMTP settings from ContactInfo
            contact_info = ContactInfo.get_active_contact_info()
            
            # Send email using dynamic SMTP settings if available
            try:
                # Check if SMTP settings are configured in ContactInfo
                if contact_info and contact_info.smtp_email and contact_info.smtp_password:
                    # Use Gmail SMTP with dynamic settings
                    # The smtp_email serves as both sender and recipient
                    connection = get_connection(
                        backend='django.core.mail.backends.smtp.EmailBackend',
                        host='smtp.gmail.com',
                        port=587,
                        username=contact_info.smtp_email,
                        password=contact_info.smtp_password,
                        use_tls=True,
                    )
                    from_email = f'Domain Finder <{contact_info.smtp_email}>'
                    recipient_email = contact_info.smtp_email  # Send to the same email that's configured for SMTP
                else:
                    # Fall back to default Django email backend (console for development)
                    connection = None
                    from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@domainfinder.com'
                    recipient_email = 'admin@domainfinder.com'  # Default fallback email
                
                send_mail(
                    subject=f'New Contact Form Submission from {contact_submission.name}',
                    message=f"""
                    New contact form submission:
                    
                    Name: {contact_submission.name}
                    Email: {contact_submission.email}
                    Message: {contact_submission.message}
                    
                    Submitted at: {contact_submission.submitted_at}
                    """,
                    from_email=from_email,
                    recipient_list=[recipient_email],
                    fail_silently=False,
                    connection=connection,
                )
            except Exception as e:
                # Log the error but don't fail the form submission
                print(f"Email sending failed: {e}")
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message! We\'ll get back to you soon.'
            })
        else:
            # Return form errors
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid data format.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again.'
        })


def handler404(request, exception):
    """Custom 404 error handler."""
    context = {
        'page_title': 'Page Not Found - Domain Finder',
    }
    return render(request, '404.html', context, status=404)


def domains_view(request):
    """Display the domains for sale page"""
    # Get all available domains, ordered by featured status and creation date
    all_domains = Domain.objects.filter(is_available=True).order_by('-is_featured_on_homepage', '-created_at')
    
    # Pagination - show first 6 domains
    domains_per_page = 6
    initial_domains = all_domains[:domains_per_page]
    has_more = all_domains.count() > domains_per_page
    
    # Calculate some stats for the header section
    domain_count = all_domains.count()
    price_range = ""
    if all_domains.exists():
        min_price = all_domains.aggregate(models.Min('price'))['price__min']
        max_price = all_domains.aggregate(models.Max('price'))['price__max'] 
        price_range = f"${min_price:,.0f} - ${max_price:,.0f}"
    
    context = {
        'page_title': 'Domains for Sale',
        'domains': initial_domains,
        'domain_count': domain_count,
        'price_range': price_range,
        'has_more': has_more,
        'domains_per_page': domains_per_page,
    }
    return render(request, 'domain_finder/domains.html', context)


@require_http_methods(["GET"])
def load_more_domains(request):
    """AJAX endpoint to load more domains"""
    try:
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 6))
        
        # Get all available domains, ordered by featured status and creation date
        all_domains = Domain.objects.filter(is_available=True).order_by('-is_featured_on_homepage', '-created_at')
        
        # Get the requested slice of domains
        domains = all_domains[offset:offset + limit]
        
        # Check if there are more domains after this batch
        has_more = all_domains.count() > (offset + limit)
        
        # Convert domains to JSON-serializable format
        domains_data = []
        for domain in domains:
            domains_data.append({
                'name': domain.name,
                'description': domain.description,
                'price': domain.price,
                'formatted_price': domain.formatted_price,
                'currency_symbol': domain.currency.symbol if domain.currency else '$',
                'display_status': domain.display_status,
                'status_badge_class': domain.status_badge_class,
                'features_list': domain.features_list,
                'listing_url': domain.listing_url,
                'view_button_text': domain.view_button_text,
                'has_external_listing': domain.has_external_listing,
                'should_show_contact_button': domain.should_show_contact_button,
                'direct_to_contact': domain.direct_to_contact,
            })
        
        return JsonResponse({
            'success': True,
            'domains': domains_data,
            'has_more': has_more,
        })
        
    except (ValueError, TypeError) as e:
        return JsonResponse({
            'success': False,
            'error': 'Invalid parameters'
        }, status=400)


def custom_404_view(request, exception=None):
    """Custom 404 page view that works even with DEBUG=True."""
    return render(request, '404.html', status=404)


def handler404(request, exception):
    """Custom 404 handler for production."""
    return render(request, '404.html', status=404)