#!/usr/bin/env python
"""
Quick deployment fix script for Nexora
Run this on the server to fix database issues immediately
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    django.setup()
    
    print("🚀 Starting Nexora deployment fix...")
    
    try:
        # Run migrations
        print("📦 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        # Force fix database
        print("🔧 Running database force fix...")
        execute_from_command_line(['manage.py', 'force_migrate'])
        
        # Generate AI analysis
        print("🤖 Generating AI analysis...")
        execute_from_command_line(['manage.py', 'generate_ai_analysis'])
        
        # Collect static files
        print("📁 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        print("✅ Deployment fix completed!")
        
    except Exception as e:
        print(f"❌ Error during deployment fix: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
