#!/bin/bash
# Quick fix for Nexora deployment issues

echo "🚨 QUICK FIX: Nexora Deployment Repair"
echo "======================================"

# Set environment
export DJANGO_SETTINGS_MODULE=app.settings

# Run migrations
echo "📦 Running migrations..."
python manage.py migrate --noinput

# Force fix database
echo "🔧 Force fixing database..."
python manage.py force_migrate

# Generate AI analysis
echo "🤖 Generating AI analysis..."
python manage.py generate_ai_analysis --force

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if needed
echo "👤 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@nexora.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

echo "✅ Quick fix completed!"
echo "Restart your web server now."
