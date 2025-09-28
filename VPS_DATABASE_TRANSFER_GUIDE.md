# 🗄️ Database Transfer Guide: Local to VPS

## 📋 What You've Completed ✅

### Local Backup Created:
- **Database Dump:** `domain_finder_backup.sql` (72K) - Contains all your data
- **Migration Files:** `migrations_backup.tar.gz` (20K) - Schema consistency backup
- **Production Config:** `.env.production` updated with database variables

### Your Current Data:
- 1 Admin User (admin/elliotmachina@gmail.com)
- 1 HomePage with dynamic content
- 1 ContactInfo with SMTP settings
- 8 Premium domains
- 3 Blog posts
- 20 Contact form submissions

---

## 🚀 VPS Setup Steps

### **Step 1: Connect to Your VPS**
```bash
# SSH into your VPS (replace with your IP)
ssh root@165.84.215.92
```

### **Step 2: Install PostgreSQL on VPS**
```bash
# Update system
apt update && apt upgrade -y

# Install PostgreSQL
apt install postgresql postgresql-contrib -y

# Start PostgreSQL service
systemctl start postgresql
systemctl enable postgresql

# Check status
systemctl status postgresql
```

### **Step 3: Create Database and User on VPS**
```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL prompt, run these commands:
CREATE DATABASE domain_finder_db;
CREATE USER domain_finder_user WITH PASSWORD 'domain_password123';
GRANT ALL PRIVILEGES ON DATABASE domain_finder_db TO domain_finder_user;
ALTER USER domain_finder_user CREATEDB;
\q
```

### **Step 4: Upload Files to VPS**

#### Option A: Using SCP (from your Mac)
```bash
# Upload database dump
scp /Users/babluvijayakumar/Projects/Python_learning/domain_finder/domain_finder_backup.sql root@165.84.215.92:/tmp/

# Upload migration backup
scp /Users/babluvijayakumar/Projects/Python_learning/domain_finder/migrations_backup.tar.gz root@165.84.215.92:/tmp/

# Upload entire project
scp -r /Users/babluvijayakumar/Projects/Python_learning/domain_finder root@165.84.215.92:/var/www/
```

#### Option B: Using rsync (recommended)
```bash
# Sync entire project (faster and more reliable)
rsync -avz --progress /Users/babluvijayakumar/Projects/Python_learning/domain_finder/ root@165.84.215.92:/var/www/domain_finder/
```

### **Step 5: Restore Database on VPS**
```bash
# On VPS, restore the database
cd /tmp
PGPASSWORD=domain_password123 psql -h localhost -U domain_finder_user -d domain_finder_db < domain_finder_backup.sql

# Verify data was imported
PGPASSWORD=domain_password123 psql -h localhost -U domain_finder_user -d domain_finder_db -c "SELECT count(*) FROM django_migrations;"
```

### **Step 6: Setup Python Environment on VPS**
```bash
# Navigate to project directory
cd /var/www/domain_finder

# Install Python and pip
apt install python3 python3-pip python3-venv -y

# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install additional production dependencies
pip install gunicorn psycopg2-binary
```

### **Step 7: Configure Production Environment**
```bash
# Copy production environment file
cp .env.production .env

# Generate a new SECRET_KEY
python3 -c "from django.core.management.utils import get_random_secret_key; print('SECRET_KEY=' + get_random_secret_key())"

# Edit .env file and replace the SECRET_KEY with the generated one
nano .env
```

### **Step 8: Test Django on VPS**
```bash
# Run migrations (should show "No migrations to apply")
python manage.py migrate

# Create superuser (optional - you already have admin in database)
# python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test server
python manage.py runserver 0.0.0.0:8000
```

---

## 🔧 Production Server Setup

### **Step 9: Install and Configure Nginx**
```bash
# Install Nginx
apt install nginx -y

# Create Nginx configuration
nano /etc/nginx/sites-available/domainfinder
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name domainfinder.uk www.domainfinder.uk 165.84.215.92;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/domain_finder;
    }
    
    location /media/ {
        root /var/www/domain_finder;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/domain_finder/domain_finder.sock;
    }
}
```

```bash
# Enable the site
ln -s /etc/nginx/sites-available/domainfinder /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

### **Step 10: Setup Gunicorn Service**
```bash
# Create Gunicorn service file
nano /etc/systemd/system/gunicorn.service
```

Add this content:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/domain_finder
ExecStart=/var/www/domain_finder/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/domain_finder/domain_finder.sock domain_finder_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable Gunicorn
systemctl start gunicorn
systemctl enable gunicorn
systemctl status gunicorn
```

---

## 🌐 Domain Configuration

### **Step 11: Update DNS (GoDaddy)**
1. Login to GoDaddy
2. Go to DNS Management for domainfinder.uk
3. Add/Update these records:
   - **A Record:** `@` → `165.84.215.92`
   - **A Record:** `www` → `165.84.215.92`

### **Step 12: Test Your Site**
- Visit: http://domainfinder.uk
- Admin: http://domainfinder.uk/admin
- All your data should be there!

---

## 🔒 SSL Setup (Optional - After Basic Setup Works)

### Using Cloudflare (Recommended):
1. Add domain to Cloudflare
2. Update nameservers at GoDaddy
3. Enable SSL/TLS → Full (strict)

### Using Let's Encrypt:
```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d domainfinder.uk -d www.domainfinder.uk
```

---

## 🎯 Quick Start Commands

### On Your Mac:
```bash
# 1. Upload everything to VPS
rsync -avz --progress /Users/babluvijayakumar/Projects/Python_learning/domain_finder/ root@165.84.215.92:/var/www/domain_finder/
```

### On Your VPS:
```bash
# 2. Setup database
sudo -u postgres createdb domain_finder_db
sudo -u postgres createuser domain_finder_user
PGPASSWORD=domain_password123 psql -h localhost -U domain_finder_user -d domain_finder_db < /var/www/domain_finder/domain_finder_backup.sql

# 3. Setup Django
cd /var/www/domain_finder
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt gunicorn psycopg2-binary
cp .env.production .env
python manage.py collectstatic --noinput
```

---

## 🆘 Troubleshooting

### Common Issues:
1. **Database connection failed:** Check PostgreSQL is running and credentials match
2. **Permission denied:** Use `chmod 755` on project directory
3. **Static files not loading:** Run `collectstatic` and check Nginx config
4. **Domain not resolving:** DNS changes can take up to 48 hours

### Verification Commands:
```bash
# Check database connection
python manage.py dbshell

# Check if data exists
python manage.py shell
>>> from domain_finder.models import Domain
>>> print(Domain.objects.count())  # Should show 8

# Check logs
journalctl -u gunicorn -f
tail -f /var/log/nginx/error.log
```

---

**Your database transfer is ready! Start with Step 1 and let me know if you need help with any step.**