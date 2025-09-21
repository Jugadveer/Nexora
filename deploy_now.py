#!/usr/bin/env python
"""
Immediate deployment fix for Render
This script will be run during build to fix database issues
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🚨 IMMEDIATE DEPLOYMENT FIX STARTING...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    django.setup()
    
    try:
        # Step 1: Run migrations
        print("📦 Running migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        # Step 2: Force fix database
        print("🔧 Running database force fix...")
        execute_from_command_line(['manage.py', 'force_migrate'])
        
        # Step 3: Emergency database fix
        print("🚨 Running emergency database fix...")
        execute_from_command_line(['manage.py', 'emergency_db_fix'])
        
        # Step 4: Generate AI analysis
        print("🤖 Generating AI analysis...")
        execute_from_command_line(['manage.py', 'generate_ai_analysis', '--force'])
        
        # Step 5: Verify everything works
        print("✅ Verifying deployment...")
        from main.models import Project
        project_count = Project.objects.count()
        print(f"✅ SUCCESS: Database working with {project_count} projects!")
        
        return True
        
    except Exception as e:
        print(f"❌ DEPLOYMENT FIX FAILED: {str(e)}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
