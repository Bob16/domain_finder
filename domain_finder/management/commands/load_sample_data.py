"""
Django management command to load sample blog data.
Save this as: domain_finder/management/commands/load_sample_data.py
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from domain_finder.models import BlogCategory, BlogPost

class Command(BaseCommand):
    help = 'Load sample blog data for Domain Finder'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Create categories
        categories_data = [
            'Domain Valuation',
            'Market Trends', 
            'Brand Strategy',
            'Investment',
            'Market Analysis',
            'Technology'
        ]
        
        for category_name in categories_data:
            category, created = BlogCategory.objects.get_or_create(
                name=category_name,
                defaults={'slug': slugify(category_name)}
            )
            if created:
                self.stdout.write(f'Created category: {category_name}')

        # Create blog posts
        blog_posts_data = [
            {
                'title': 'The Ultimate Guide to Domain Valuation in 2025',
                'author': 'Sarah Johnson',
                'excerpt': 'Learn the key factors that determine domain value and how to assess the worth of premium domains in today\'s market.',
                'category': 'Domain Valuation',
                'image_url': 'https://images.unsplash.com/photo-1533750349088-cd871a92f312?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkaWdpdGFsJTIwbWFya2V0aW5nJTIwc3RyYXRlZ3l8ZW58MXx8fHwxNzU4MDUxMTc3fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
                'read_time': '8 min read',
                'is_featured': True,
                'content': '''## Understanding Domain Valuation

Domain valuation is both an art and a science. In 2025, the landscape has evolved significantly with new factors influencing how we assess domain worth. This comprehensive guide will walk you through the essential elements that determine domain value.

Key Factors in Domain Valuation

Several critical factors contribute to a domain's value:

Length and Memorability: Shorter domains are generally more valuable
Keyword Relevance: Domains containing popular search terms  
Extension: .com domains typically command higher prices
Commercial Potential: Ability to generate revenue
Brand Potential: How well the domain could serve as a brand

Market Analysis Techniques

To accurately value a domain, you need to understand market dynamics. Look at recent sales of comparable domains, analyze search volume for related keywords, and consider the commercial viability of the domain name.

>
 Pro Tip: Always compare similar domains that have sold within the last 12 months for the most accurate valuation.

Tools and Resources

Professional domain investors rely on various tools to assess value:

Domain appraisal services
Sales comparison databases  
SEO and keyword research tools
Market trend analysis platforms

Future Trends

Looking ahead, factors like AI integration, web3 compatibility, and geographic relevance are becoming increasingly important in domain valuation. Stay ahead by understanding these emerging trends.

The domain market is evolving rapidly, and those who adapt to these changes will find the best investment opportunities.'''
            },
            {
                'title': 'Emerging Domain Trends: What to Watch in 2025',
                'author': 'Michael Chen',
                'excerpt': 'Discover the latest trends in domain investments, from new TLDs to geographic domains that are gaining traction.',
                'category': 'Market Trends',
                'image_url': 'https://images.unsplash.com/photo-1712159018726-4564d92f3ec2?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXNpbmVzcyUyMHRlY2hub2xvZ3klMjBvZmZpY2V8ZW58MXx8fHwxNzU4MTQzNzQ0fDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
                'read_time': '6 min read',
                'content': '''
                <h2>The Domain Landscape in 2025</h2>
                <p>The domain industry continues to evolve at a rapid pace. Understanding current trends is crucial for making informed investment decisions and staying competitive in the market.</p>
                
                <h3>New TLD Performance</h3>
                <p>Beyond traditional extensions, several new TLDs are gaining significant traction:</p>
                <ul>
                  <li><strong>.ai domains:</strong> High demand due to AI boom</li>
                  <li><strong>.crypto and .nft:</strong> Web3 and blockchain applications</li>
                  <li><strong>.store and .shop:</strong> E-commerce focused domains</li>
                  <li><strong>Geographic TLDs:</strong> City and country-specific extensions</li>
                </ul>
                
                <h3>Investment Strategies</h3>
                <p>Successful domain investors are adapting their strategies to capitalize on these trends. Focus areas include technology-related keywords, sustainable business terms, and localized domain names.</p>
                
                <h3>Market Predictions</h3>
                <p>Industry experts predict continued growth in premium domain values, especially for short, brandable names and those related to emerging technologies. Geographic domains are also expected to see increased demand as local businesses expand their digital presence.</p>
                '''
            },
            {
                'title': 'Brand Protection: Securing Your Domain Portfolio',
                'author': 'Emily Rodriguez',
                'excerpt': 'Essential strategies for protecting your brand through strategic domain acquisition and management.',
                'category': 'Brand Strategy',
                'image_url': 'https://images.unsplash.com/photo-1684610529682-553625a1ffed?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkb21haW4lMjBhbmFseXRpY3MlMjBkYXRhJTIwdmlzdWFsaXphdGlvbnxlbnwxfHx8fDE3NTgxNDM3NDJ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral',
                'read_time': '10 min read',
                'content': '''
                <h2>Why Brand Protection Matters</h2>
                <p>In today's digital landscape, protecting your brand through strategic domain management is more important than ever. A comprehensive domain strategy can prevent brand dilution and protect against cyber threats.</p>
                
                <h3>Core Protection Strategies</h3>
                <p>Effective brand protection involves multiple layers:</p>
                <ul>
                  <li><strong>Primary Domain Security:</strong> Securing your main brand domains</li>
                  <li><strong>Defensive Registrations:</strong> Common misspellings and variations</li>
                  <li><strong>TLD Coverage:</strong> Multiple extensions for key brand terms</li>
                  <li><strong>Monitoring Services:</strong> Watching for new registrations</li>
                </ul>
                
                <h3>Risk Assessment</h3>
                <p>Understanding potential threats helps prioritize protection efforts. Consider risks like typosquatting, cybersquatting, and brand impersonation when developing your strategy.</p>
                
                <h3>Implementation Guidelines</h3>
                <p>Start with your core brand terms and expand based on business priorities. Regular audits and updates ensure your protection strategy remains effective as your brand evolves.</p>
                '''
            },
        ]
        
        for post_data in blog_posts_data:
            category = BlogCategory.objects.get(name=post_data['category'])
            
            blog_post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'slug': slugify(post_data['title']),
                    'author': post_data['author'],
                    'excerpt': post_data['excerpt'],
                    'content': post_data['content'],
                    'category': category,
                    'image_url': post_data['image_url'],
                    'read_time': post_data['read_time'],
                    'is_featured': post_data.get('is_featured', False),
                    'is_published': True,
                }
            )
            
            if created:
                self.stdout.write(f'Created blog post: {post_data["title"]}')
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data!'))