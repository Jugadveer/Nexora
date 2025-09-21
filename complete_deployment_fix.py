#!/usr/bin/env python
"""
Complete deployment fix script for Nexora
This script fixes database issues and regenerates all AI analysis
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    django.setup()
    
    print("🚀 Starting complete Nexora deployment fix...")
    
    try:
        # Step 1: Run migrations
        print("📦 Step 1: Running database migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        # Step 2: Force fix database
        print("🔧 Step 2: Running database force fix...")
        execute_from_command_line(['manage.py', 'force_migrate'])
        
        # Step 3: Regenerate all AI analysis
        print("🤖 Step 3: Regenerating all AI analysis...")
        execute_from_command_line(['manage.py', 'generate_ai_analysis', '--force'])
        
        # Step 4: Collect static files
        print("📁 Step 4: Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        
        # Step 5: Verify everything is working
        print("✅ Step 5: Verifying deployment...")
        from main.models import Project, AIAnalystReport
        
        total_projects = Project.objects.count()
        projects_with_analysis = AIAnalystReport.objects.count()
        
        print(f"📊 Verification Results:")
        print(f"  Total projects: {total_projects}")
        print(f"  Projects with AI analysis: {projects_with_analysis}")
        print(f"  Coverage: {(projects_with_analysis/total_projects)*100:.1f}%")
        
        if projects_with_analysis == total_projects:
            print("🎉 SUCCESS: All projects have AI analysis!")
        else:
            print(f"⚠️  WARNING: {total_projects - projects_with_analysis} projects missing AI analysis")
        
        print("\n✅ Complete deployment fix finished!")
        print("\nNext steps:")
        print("1. Restart your web server")
        print("2. Test the login functionality")
        print("3. Create a new project to test real-time AI analysis")
        print("4. Check the AI analysis display on project pages")
        
    except Exception as e:
        print(f"❌ Error during deployment fix: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
