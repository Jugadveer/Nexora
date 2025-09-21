#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check Django installation
echo "Checking Django installation..."
python -c "import django; print(f'Django version: {django.get_version()}')"

# Check database connection
echo "Checking database connection..."
python manage.py check --database default

# Apply database migrations with force fix
echo "Applying database migrations..."
python manage.py migrate --verbosity=2 || echo "Standard migration failed, trying force fix..."

# Force fix database if needed
echo "Running database force fix..."
python manage.py force_migrate || echo "Force migrate failed, continuing..."

# Show migration status
echo "Migration status:"
python manage.py showmigrations

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@nexora.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
"

# Verify database tables exist
echo "Verifying database tables..."
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
tables = cursor.fetchall()
print('Database tables:', [table[0] for table in tables])
"

# Generate AI analysis for existing projects (in background to avoid timeout)
echo "Generating AI analysis for existing projects..."
python manage.py generate_ai_analysis --force || echo "AI analysis generation failed, continuing..."

echo "Build complete!"
