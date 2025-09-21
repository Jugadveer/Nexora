# Deployment fix script for Nexora (PowerShell version)
# This script fixes database migration issues and generates AI analysis

Write-Host "🚀 Starting Nexora deployment fix..." -ForegroundColor Green

# Set environment variables
$env:DJANGO_SETTINGS_MODULE = "app.settings"
$env:PYTHONPATH = "$PWD;$env:PYTHONPATH"

# Activate virtual environment if it exists
if (Test-Path "venv") {
    Write-Host "📦 Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
}

# Install/update dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run database migrations
Write-Host "🗄️  Running database migrations..." -ForegroundColor Yellow
python manage.py migrate --noinput

# Check database status
Write-Host "🔍 Checking database status..." -ForegroundColor Yellow
python manage.py fix_database --check-only

# Generate AI analysis for existing projects
Write-Host "🤖 Generating AI analysis for existing projects..." -ForegroundColor Yellow
python manage.py generate_ai_analysis

# Collect static files
Write-Host "📁 Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
Write-Host "👤 Creating superuser if needed..." -ForegroundColor Yellow
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@nexora.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

Write-Host "✅ Deployment fix completed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Restart your web server (gunicorn/uwsgi)" -ForegroundColor White
Write-Host "2. Check the application logs for any errors" -ForegroundColor White
Write-Host "3. Test the login functionality" -ForegroundColor White
Write-Host ""
Write-Host "If you're using Render, the deployment should automatically restart." -ForegroundColor Yellow
