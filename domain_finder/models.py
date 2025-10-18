"""
Django models for the Domain Finder application.
"""
from django.db import models
from django.urls import reverse
from django.utils import timezone
import markdown
from django.utils.safestring import mark_safe

class HomePage(models.Model):
    """Homepage hero section content."""
    title = models.CharField(
        max_length=200,
        help_text="Main headline. You can use HTML like <span class='text-primary'>Domain</span>"
    )
    subtitle = models.TextField(
        max_length=500,
        help_text="Description text below the main headline"
    )
    hero_image = models.ImageField(
        upload_to='homepage/hero/',
        blank=True,
        null=True,
        help_text="Hero image for the homepage. Leave empty to use default image."
    )
    
    # Statistics Section
    domains_analyzed = models.CharField(
        max_length=20,
        default="500+",
        help_text="Number of domains analyzed (e.g., '500+', '1000+')"
    )
    domains_analyzed_label = models.CharField(
        max_length=50,
        default="Domains Analyzed",
        help_text="Label for domains analyzed statistic"
    )
    client_satisfaction = models.CharField(
        max_length=20,
        default="98%",
        help_text="Client satisfaction percentage (e.g., '98%', '99%')"
    )
    client_satisfaction_label = models.CharField(
        max_length=50,
        default="Client Satisfaction",
        help_text="Label for client satisfaction statistic"
    )
    response_time = models.CharField(
        max_length=20,
        default="24h",
        help_text="Average response time (e.g., '24h', '12h')"
    )
    response_time_label = models.CharField(
        max_length=50,
        default="Avg. Response Time",
        help_text="Label for response time statistic"
    )
    
    # Market Intelligence Section
    market_intelligence_pill = models.CharField(
        max_length=50,
        default="Market Intelligence",
        help_text="Text for the pill button (without emoji)"
    )
    market_intelligence_title = models.CharField(
        max_length=100,
        default="Data-Driven Domain Research",
        help_text="Main title for Market Intelligence section"
    )
    market_intelligence_subtitle = models.TextField(
        max_length=300,
        default="Our comprehensive analytics provide deep insights into domain performance, market trends, and competitive landscape.",
        help_text="Subtitle description for Market Intelligence section"
    )
    
    # Analytics Card 1 - Market Trends
    card1_title = models.CharField(
        max_length=50,
        default="Market Trends",
        help_text="Title for first analytics card"
    )
    card1_subtitle = models.CharField(
        max_length=150,
        default="Real-time analysis of domain market trends and pricing patterns",
        help_text="Subtitle for first analytics card"
    )
    card1_number = models.CharField(
        max_length=20,
        default="94%",
        help_text="Number/percentage for first analytics card"
    )
    card1_label = models.CharField(
        max_length=50,
        default="Accuracy Rate",
        help_text="Label for first analytics card number"
    )
    
    # Analytics Card 2 - Brand Alignment
    card2_title = models.CharField(
        max_length=50,
        default="Brand Alignment",
        help_text="Title for second analytics card"
    )
    card2_subtitle = models.CharField(
        max_length=150,
        default="Evaluate how well domains match your brand identity and goals",
        help_text="Subtitle for second analytics card"
    )
    card2_number = models.CharField(
        max_length=20,
        default="89%",
        help_text="Number/percentage for second analytics card"
    )
    card2_label = models.CharField(
        max_length=50,
        default="Match Score",
        help_text="Label for second analytics card number"
    )
    
    # Analytics Card 3 - Risk Assessment
    card3_title = models.CharField(
        max_length=50,
        default="Risk Assessment",
        help_text="Title for third analytics card"
    )
    card3_subtitle = models.CharField(
        max_length=150,
        default="Comprehensive domain history and legal risk evaluation",
        help_text="Subtitle for third analytics card"
    )
    card3_number = models.CharField(
        max_length=20,
        default="99%",
        help_text="Number/percentage for third analytics card"
    )
    card3_label = models.CharField(
        max_length=50,
        default="Clean Domains",
        help_text="Label for third analytics card number"
    )
    
    # Advanced Analytics Section Toggle
    show_advanced_analytics = models.BooleanField(
        default=False,
        help_text="Show/Hide the Advanced Analytics section on homepage"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Set to True to use this content on homepage"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Home Page Content ({'Active' if self.is_active else 'Inactive'})"
    
    def save(self, *args, **kwargs):
        # Ensure only one active homepage content at a time
        if self.is_active:
            HomePage.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

class BlogCategory(models.Model):
    """Blog post categories."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Author(models.Model):
    """Blog post authors."""
    name = models.CharField(max_length=100, help_text="Author's full name")
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        help_text="Author biography. If empty, a default bio will be used."
    )
    avatar = models.URLField(
        max_length=500, 
        blank=True, 
        help_text="Author profile image URL. If empty, a default avatar will be used."
    )
    email = models.EmailField(blank=True, help_text="Author's email address (optional)")
    website = models.URLField(blank=True, help_text="Author's personal website (optional)")
    is_active = models.BooleanField(default=True, help_text="Whether this author is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Author"
        verbose_name_plural = "Authors"
    
    def __str__(self):
        return self.name
    
    @property
    def display_bio(self):
        """Get author bio with fallback to default text."""
        if self.bio.strip():
            return self.bio
        return f"Domain research expert with over 10 years of experience in digital asset evaluation and market analysis. Specializes in emerging market trends and investment strategies."
    
    @property
    def display_avatar(self):
        """Get author avatar URL or None for fallback to default."""
        return self.avatar if self.avatar.strip() else None

class BlogPost(models.Model):
    """Blog post model."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='blog_posts',
        help_text="Select the author for this blog post"
    )
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    image_url = models.URLField(max_length=500, blank=True)
    read_time = models.CharField(max_length=20, default="5 min read")
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('domain_finder:blog_detail', kwargs={'post_id': self.pk})
    
    @property
    def formatted_date(self):
        return self.created_at.strftime("%B %d, %Y")

    @property
    def content_as_markdown(self):
        """Convert markdown content to HTML."""
        return mark_safe(markdown.markdown(self.content, extensions=['extra', 'codehilite']))

class ContactSubmission(models.Model):
    """Contact form submissions."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"Contact from {self.name} - {self.email}"

class ContactInfo(models.Model):
    """Contact page content management."""
    
    # Email section
    email_value = models.EmailField(default="info@domainfinder.com")
    email_description = models.CharField(max_length=200, default="We typically respond within 24 hours")
    
    # Phone section  
    phone_value = models.CharField(max_length=50, default="+1 (555) 123-4567")
    phone_description = models.CharField(max_length=200, default="Mon-Fri 9AM-6PM PST")
    
    # Address section
    address_line1 = models.CharField(max_length=200, default="123 Domain Street")
    address_line2 = models.CharField(max_length=200, default="San Francisco, CA 94105")
    
    # Services section
    show_services = models.BooleanField(
        default=True,
        help_text="Show/hide the Our Services section on contact page"
    )
    services_title = models.CharField(
        max_length=100,
        default="Our Services",
        help_text="Title for the services section"
    )
    services_subtitle = models.CharField(
        max_length=200,
        default="What we can help you with",
        help_text="Subtitle for the services section"
    )

        # What to Expect section - ADD THESE NEW FIELDS HERE
    show_what_to_expect = models.BooleanField(
        default=True,
        help_text="Show/hide the What to Expect section on contact page"
    )
    what_to_expect_title = models.CharField(
        max_length=100,
        default="What to Expect",
        help_text="Title for the What to Expect section"
    )
    
    # SMTP settings for sending emails
    smtp_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Gmail address for sending emails and receiving contact form messages"
    )
    smtp_password = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Gmail App Password (16-character password from Google Account settings)"
    )
    
    # Email branding settings
    from_email = models.CharField(
        max_length=255,
        default="Domain Finder <noreply@domainfinder.uk>",
        help_text="The 'From' address that appears in outgoing emails. Format: 'Your Business Name <email@domain.com>'"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Contact Page Content"
        verbose_name_plural = "Contact Page Content"
        ordering = ['-created_at']
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"Contact Page Content ({status})"
    
    @classmethod
    def get_active_contact_info(cls):
        """Get the active contact information."""
        return cls.objects.filter(is_active=True).first()


class ContactService(models.Model):
    """Individual service items for the contact page services section."""
    
    contact_info = models.ForeignKey(
        ContactInfo,
        on_delete=models.CASCADE,
        related_name='services',
        help_text="Associated contact page content"
    )
    name = models.CharField(
        max_length=200,
        help_text="Service name (e.g., 'Domain Market Research & Analysis')"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show/hide this service on the contact page"
    )
    sort_order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


class DomainStatus(models.Model):
    """Status categories for domains."""
    
    name = models.CharField(max_length=20, unique=True, help_text="Status name (e.g., Premium, Featured)")
    slug = models.SlugField(max_length=20, unique=True, help_text="URL-friendly version (e.g., premium, featured)")
    badge_class = models.CharField(
        max_length=100, 
        help_text="CSS classes for the status badge (e.g., bg-green-100 text-green-800)",
        default="bg-gray-100 text-gray-800"
    )
    is_active = models.BooleanField(default=True, help_text="Is this status available for selection?")
    sort_order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Domain Status"
        verbose_name_plural = "Domain Statuses"
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


class Currency(models.Model):
    """Currency types for domains."""
    
    name = models.CharField(max_length=30, unique=True, help_text="Currency name (e.g., US Dollar, British Pound)")
    code = models.CharField(max_length=3, unique=True, help_text="Currency code (e.g., USD, GBP, EUR)")
    symbol = models.CharField(max_length=5, help_text="Currency symbol (e.g., $, £, €)")
    is_active = models.BooleanField(default=True, help_text="Is this currency available for selection?")
    sort_order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Domain(models.Model):
    """Model for domains for sale."""
    
    name = models.CharField(
        max_length=100, 
        unique=True,
        help_text="Domain name (e.g., TechStartup.com)"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price value (e.g., 5000.00)"
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        help_text="Currency for the price",
        limit_choices_to={'is_active': True},
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        DomainStatus,
        on_delete=models.PROTECT,
        help_text="Domain status/category",
        limit_choices_to={'is_active': True}
    )
    description = models.TextField(
        help_text="Brief description of the domain and its potential use"
    )
    features = models.TextField(
        help_text="Domain features/benefits (one per line)",
        blank=True
    )
    listing_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="External listing URL (e.g., GoDaddy, Sedo, Flippa)"
    )
    website_name = models.CharField(
        max_length=50,
        blank=True,
        default="GoDaddy",
        help_text="Name of the marketplace/website (e.g., GoDaddy, Sedo, Flippa)"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Is the domain currently available for sale?"
    )
    is_featured_on_homepage = models.BooleanField(
        default=False,
        help_text="Display this domain on the homepage"
    )
    direct_to_contact = models.BooleanField(
        default=False,
        help_text="If checked, the button will direct to contact page instead of external listing"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured_on_homepage', '-created_at']
        verbose_name = "Domain for Sale"
        verbose_name_plural = "Domains for Sale"
    
    def __str__(self):
        currency_symbol = self.currency.symbol if self.currency else '$'
        return f"{self.name} - {currency_symbol}{self.price:,.0f}"
    
    @property
    def formatted_price(self):
        """Return formatted price with currency symbol and commas."""
        currency_symbol = self.currency.symbol if self.currency else '$'
        return f"{currency_symbol}{self.price:,.0f}"
    
    @property
    def features_list(self):
        """Return features as a list."""
        if self.features:
            return [feature.strip() for feature in self.features.split('\n') if feature.strip()]
        return []
    
    @property
    def status_badge_class(self):
        """Return CSS class for status badge."""
        return self.status.badge_class if self.status else 'bg-gray-100 text-gray-800'
    
    @property
    def display_status(self):
        """Return display name for status."""
        return self.status.name if self.status else 'Regular'
    
    @property
    def has_external_listing(self):
        """Check if domain has an external listing URL and is not set to direct to contact."""
        return bool(self.listing_url) and not self.direct_to_contact
    
    @property
    def should_show_contact_button(self):
        """Check if domain should show contact button."""
        return self.direct_to_contact or not self.listing_url
    
    @property
    def view_button_text(self):
        """Return dynamic button text based on contact preference and website name."""
        if self.direct_to_contact:
            return "Contact for Details"
        elif self.listing_url and self.website_name:
            return f"View on {self.website_name}"
        elif self.listing_url:
            return "View Listing"
        else:
            return "Contact for Details"
    
    @property
    def button_url(self):
        """Return the appropriate URL for the button."""
        if self.direct_to_contact or not self.listing_url:
            return "/contact/"  # This will be handled in template with {% url %}
        else:
            return self.listing_url
        

class ExpectationItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="CSS class for icon (e.g., 'fas fa-clock')")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Expectation Item'
        verbose_name_plural = 'Expectation Items'
    
    def __str__(self):
        return self.title