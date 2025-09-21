#!/bin/bash

# Deployment fix script for Nexora
# This script fixes database migration issues and generates AI analysis

echo "🚀 Starting Nexora deployment fix..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=app.settings
export PYTHONPATH=$PWD:$PYTHONPATH

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput

# Check database status
echo "🔍 Checking database status..."
python manage.py fix_database --check-only

# Generate AI analysis for existing projects
echo "🤖 Generating AI analysis for existing projects..."
python manage.py generate_ai_analysis

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser if needed..."
python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@nexora.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

echo "✅ Deployment fix completed!"
echo ""
echo "Next steps:"
echo "1. Restart your web server (gunicorn/uwsgi)"
echo "2. Check the application logs for any errors"
echo "3. Test the login functionality"
echo ""
echo "If you're using Render, the deployment should automatically restart."
