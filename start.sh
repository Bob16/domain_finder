#!/bin/bash

echo "🚀 Starting Domain Finder Django Application..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Load sample data
echo "📝 Loading sample blog data..."
python manage.py load_sample_data

# Create superuser (interactive)
echo "👤 Create admin user:"
python manage.py createsuperuser

# Start development server
echo "🌐 Starting development server..."
echo "Access your site at: http://127.0.0.1:8000/"
echo "Admin panel at: http://127.0.0.1:8000/admin/"
python manage.py runserver