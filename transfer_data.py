#!/usr/bin/env python
"""
Data transfer script for Nexora
This script helps transfer all local data to the deployed server
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🚀 Nexora Data Transfer Script")
    print("=" * 40)
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    django.setup()
    
    print("📤 Step 1: Exporting data from local database...")
    try:
        execute_from_command_line(['manage.py', 'export_data'])
        print("✅ Data exported successfully!")
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return False
    
    print("\n📁 Step 2: Data export file created")
    print("   File: nexora_data_export.json")
    print("   Next: Upload this file to your deployed server")
    
    print("\n📋 Step 3: Instructions for deployed server")
    print("   1. Upload nexora_data_export.json to your server")
    print("   2. Run: python manage.py import_data")
    print("   3. Or run: python manage.py import_data --clear-existing")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
