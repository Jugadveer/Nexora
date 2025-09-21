#!/usr/bin/env python
"""
Emergency fix script for Nexora deployment
Fixes database issues and ensures AI analysis works without external APIs
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    django.setup()
    
    print("🚨 EMERGENCY FIX: Starting Nexora deployment repair...")
    
    try:
        # Step 1: Check current database status
        print("📊 Step 1: Checking database status...")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            existing_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"Existing tables: {existing_tables}")
        
        # Step 2: Run migrations
        print("📦 Step 2: Running database migrations...")
        try:
            execute_from_command_line(['manage.py', 'migrate', '--noinput'])
            print("✅ Migrations completed successfully")
        except Exception as e:
            print(f"⚠️  Migration failed: {e}")
            print("Trying force migration...")
        
        # Step 3: Force fix database if needed
        print("🔧 Step 3: Running database force fix...")
        try:
            execute_from_command_line(['manage.py', 'force_migrate'])
            print("✅ Force migration completed")
        except Exception as e:
            print(f"❌ Force migration failed: {e}")
            # Try manual table creation
            create_tables_manually()
        
        # Step 4: Verify database is working
        print("🔍 Step 4: Verifying database...")
        try:
            from main.models import Project
            project_count = Project.objects.count()
            print(f"✅ Database working! Found {project_count} projects")
        except Exception as e:
            print(f"❌ Database still not working: {e}")
            return False
        
        # Step 5: Regenerate AI analysis (without external APIs)
        print("🤖 Step 5: Regenerating AI analysis...")
        try:
            execute_from_command_line(['manage.py', 'generate_ai_analysis', '--force'])
            print("✅ AI analysis regeneration completed")
        except Exception as e:
            print(f"⚠️  AI analysis regeneration failed: {e}")
        
        # Step 6: Collect static files
        print("📁 Step 6: Collecting static files...")
        try:
            execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
            print("✅ Static files collected")
        except Exception as e:
            print(f"⚠️  Static collection failed: {e}")
        
        # Step 7: Final verification
        print("✅ Step 7: Final verification...")
        try:
            from main.models import Project, AIAnalystReport
            total_projects = Project.objects.count()
            projects_with_analysis = AIAnalystReport.objects.count()
            
            print(f"📊 Final Results:")
            print(f"  Total projects: {total_projects}")
            print(f"  Projects with AI analysis: {projects_with_analysis}")
            print(f"  Coverage: {(projects_with_analysis/total_projects)*100:.1f}%")
            
            if total_projects > 0:
                print("🎉 SUCCESS: Database is working and projects are accessible!")
            else:
                print("⚠️  WARNING: No projects found in database")
                
        except Exception as e:
            print(f"❌ Final verification failed: {e}")
            return False
        
        print("\n🎉 EMERGENCY FIX COMPLETED!")
        print("\nNext steps:")
        print("1. Restart your web server (gunicorn/uwsgi)")
        print("2. Test the website - login should work now")
        print("3. Check that AI analysis is displaying properly")
        print("4. Create a new project to test real-time AI analysis")
        
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR during emergency fix: {str(e)}")
        return False

def create_tables_manually():
    """Create essential tables manually if migrations fail"""
    print("🔨 Creating tables manually...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            # Create auth_user table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auth_user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password VARCHAR(128) NOT NULL,
                    last_login DATETIME,
                    is_superuser BOOLEAN NOT NULL,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    email VARCHAR(254) NOT NULL,
                    is_staff BOOLEAN NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    date_joined DATETIME NOT NULL
                );
            """)
            
            # Create main_project table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS main_project (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(40) NOT NULL,
                    description TEXT NOT NULL,
                    problem TEXT,
                    market TEXT,
                    competition TEXT,
                    details TEXT,
                    stage VARCHAR(100) NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    url VARCHAR(200),
                    banner VARCHAR(100),
                    funding_goal DECIMAL(10,2) NOT NULL,
                    created_at DATETIME NOT NULL,
                    user_id INTEGER NOT NULL REFERENCES auth_user(id)
                );
            """)
            
            # Create main_aianalystreport table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS main_aianalystreport (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    risk_score REAL NOT NULL,
                    risk_level VARCHAR(20) NOT NULL,
                    tam_inflation_risk REAL NOT NULL,
                    financial_consistency_risk REAL NOT NULL,
                    market_saturation_risk REAL NOT NULL,
                    competition_risk REAL NOT NULL,
                    team_risk REAL NOT NULL,
                    growth_score REAL NOT NULL,
                    growth_index VARCHAR(20) NOT NULL,
                    traction_score REAL NOT NULL,
                    hiring_momentum REAL NOT NULL,
                    market_demand_score REAL NOT NULL,
                    scalability_potential REAL NOT NULL,
                    sector_rank INTEGER NOT NULL,
                    sector_percentile REAL NOT NULL,
                    platform_rank INTEGER NOT NULL,
                    platform_percentile REAL NOT NULL,
                    vs_sector_avg REAL NOT NULL,
                    vs_platform_avg REAL NOT NULL,
                    vs_similar_stage REAL NOT NULL,
                    risk_analysis TEXT NOT NULL,
                    growth_analysis TEXT NOT NULL,
                    peer_analysis TEXT NOT NULL,
                    recommendations TEXT NOT NULL,
                    generated_at DATETIME NOT NULL,
                    last_updated DATETIME NOT NULL,
                    ai_model_version VARCHAR(50) NOT NULL,
                    project_id INTEGER NOT NULL UNIQUE REFERENCES main_project(id)
                );
            """)
            
            print("✅ Essential tables created manually")
            
    except Exception as e:
        print(f"❌ Manual table creation failed: {e}")

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
