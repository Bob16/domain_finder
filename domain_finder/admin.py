"""
Django admin configuration for Domain Finder.
"""
from django.contrib import admin
from django import forms
from .models import HomePage, BlogCategory, Author, BlogPost, ContactSubmission, ContactInfo, ContactService, Domain, DomainStatus, Currency

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    fieldsets = [
        ('Hero Section', {
            'fields': ['title', 'subtitle', 'hero_image']
        }),
        ('Statistics Section', {
            'fields': [
                ('domains_analyzed', 'domains_analyzed_label'),
                ('client_satisfaction', 'client_satisfaction_label'),
                ('response_time', 'response_time_label')
            ]
        }),
        ('Market Intelligence Section', {
            'fields': [
                'market_intelligence_pill',
                'market_intelligence_title',
                'market_intelligence_subtitle'
            ]
        }),
        ('Analytics Card 1 - Market Trends', {
            'fields': [
                ('card1_title', 'card1_subtitle'),
                ('card1_number', 'card1_label')
            ]
        }),
        ('Analytics Card 2 - Brand Alignment', {
            'fields': [
                ('card2_title', 'card2_subtitle'),
                ('card2_number', 'card2_label')
            ]
        }),
        ('Analytics Card 3 - Risk Assessment', {
            'fields': [
                ('card3_title', 'card3_subtitle'),
                ('card3_number', 'card3_label')
            ]
        }),
        ('Settings', {
            'fields': ['show_advanced_analytics', 'is_active']
        })
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion if it's the only active homepage content
        if obj and obj.is_active and HomePage.objects.filter(is_active=True).count() == 1:
            return False
        return super().has_delete_permission(request, obj)

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email']
    list_editable = ['is_active']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'website', 'is_active')
        }),
        ('Profile', {
            'fields': ('bio', 'avatar'),
            'description': 'Author biography and profile image. Leave empty to use defaults.'
        }),
    )

class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 20,
            'cols': 100,
            'style': 'font-family: monospace;'
        }),
        help_text="""
        <strong>Markdown Formatting Guide:</strong><br>
        # Heading 1<br>
        ## Heading 2<br>
        ### Heading 3<br>
        **Bold text**<br>
        *Italic text*<br>
        - **Length and Memorability**: Shorter domains are generally more valuable<br>
        - **Industry Relevance**: Domain should match the business type<br>
        1. **Numbered list item**: Description here<br>
        [Link text](http://example.com)<br>
        `Inline code`<br>
        > Blockquote<br><br>
        <strong>For bullet points with bold labels:</strong><br>
        - **Label**: Description<br>
        - **Another Label**: Another description<br><br>
        Separate paragraphs with blank lines.
        """
    )
    
    class Meta:
        model = BlogPost
        fields = '__all__'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ['title', 'author', 'category', 'is_featured', 'is_published', 'created_at']
    list_filter = ['author', 'category', 'is_featured', 'is_published', 'created_at']
    search_fields = ['title', 'author__name', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        ('Author & Category', {
            'fields': ('author', 'category'),
            'description': 'Select the author and category for this blog post.'
        }),
        ('Media & Settings', {
            'fields': ('image_url', 'read_time', 'is_featured', 'is_published')
        }),
    )

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'submitted_at', 'is_responded']
    list_filter = ['is_responded', 'submitted_at']
    search_fields = ['name', 'email']
    readonly_fields = ['name', 'email', 'message', 'submitted_at']
    list_editable = ['is_responded']
    ordering = ['-submitted_at']
    
    def has_add_permission(self, request):
        # Don't allow adding submissions through admin
        return False

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'show_services', 'updated_at']
    list_filter = ['is_active', 'show_services', 'updated_at']
    ordering = ['-updated_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': (
                ('email_value', 'email_description'),
                ('phone_value', 'phone_description'),
                ('address_line1', 'address_line2')
            )
        }),
        ('Services Section', {
            'fields': (
                'show_services',
                'services_title',
                'services_subtitle'
            ),
            'description': 'Configure the Our Services section title and subtitle. Individual services are managed separately in the Services admin section.',
        }),
        ('Email Configuration', {
            'fields': ('smtp_email', 'smtp_password', 'from_email'),
            'description': 'Configure Gmail for sending emails. Contact form messages will be sent to the SMTP email address. Generate App Password from Google Account Security settings.',
        }),
        ('Settings', {
            'fields': ['is_active']
        })
    )
    
    def save_model(self, request, obj, form, change):
        if obj.is_active:
            # Deactivate all other ContactInfo instances
            ContactInfo.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)


@admin.register(ContactService)
class ContactServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'sort_order', 'contact_info', 'updated_at']
    list_filter = ['is_active', 'contact_info', 'created_at']
    list_editable = ['is_active', 'sort_order']
    search_fields = ['name']
    ordering = ['sort_order', 'name']
    
    fieldsets = (
        ('Service Details', {
            'fields': ('contact_info', 'name', 'is_active', 'sort_order')
        }),
    )


@admin.register(DomainStatus)
class DomainStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'badge_class', 'is_active', 'sort_order']
    list_filter = ['is_active']
    search_fields = ['name', 'slug']
    list_editable = ['is_active', 'sort_order', 'badge_class']
    ordering = ['sort_order', 'name']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sort_order', 'is_active')
        }),
        ('Styling', {
            'fields': ('badge_class',),
            'description': 'CSS classes for the status badge. Examples:<br>' +
                         '• Premium: <code>bg-green-100 text-green-800</code><br>' +
                         '• Featured: <code>bg-blue-100 text-blue-800</code><br>' +
                         '• New: <code>bg-purple-100 text-purple-800</code><br>' +
                         '• Hot: <code>bg-red-100 text-red-800</code><br>' +
                         '• Trending: <code>bg-orange-100 text-orange-800</code><br>' +
                         '• Limited: <code>bg-yellow-100 text-yellow-800</code>'
        }),
    )


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'symbol', 'is_active', 'sort_order']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'symbol']
    list_editable = ['is_active', 'sort_order']
    ordering = ['sort_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'symbol', 'sort_order', 'is_active')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        # Make code readonly if editing existing currency to prevent breaking references
        if obj:  # Editing existing currency
            return ['code']
        return []


class DomainAdminForm(forms.ModelForm):
    features = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'cols': 80,
            'placeholder': 'Enter features one per line, for example:\nHigh search volume keywords\nClean domain history\nInstant brand recognition\nSEO-friendly structure\nGlobal market appeal'
        }),
        help_text="Enter domain features/benefits, one per line. These will appear as bullet points on the domain listing.",
        required=False
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 80,
            'placeholder': 'Perfect for technology companies and startup ventures. Short, memorable, and highly brandable domain.'
        }),
        help_text="Brief description of the domain and its potential use cases."
    )
    
    class Meta:
        model = Domain
        fields = '__all__'


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    form = DomainAdminForm
    list_display = ['name', 'formatted_price', 'currency', 'status', 'is_available', 'is_featured_on_homepage', 'created_at']
    list_filter = ['currency', 'status', 'is_available', 'is_featured_on_homepage', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'is_featured_on_homepage']
    ordering = ['-is_featured_on_homepage', '-created_at']
    
    fieldsets = (
        ('Domain Information', {
            'fields': ('name', 'price', 'currency', 'status')
        }),
        ('Content', {
            'fields': ('description', 'features')
        }),
        ('External Listing', {
            'fields': ('listing_url', 'website_name', 'direct_to_contact'),
            'description': 'Configure external marketplace listing (e.g., GoDaddy, Sedo, Flippa, etc.). Check "Direct to contact" to override external listing and show contact button instead.'
        }),
        ('Availability', {
            'fields': ('is_available', 'is_featured_on_homepage')
        }),
    )
    
    def formatted_price(self, obj):
        return obj.formatted_price
    formatted_price.short_description = 'Price'
    formatted_price.admin_order_field = 'price'