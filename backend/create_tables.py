#!/usr/bin/env python3
"""
Database initialization script for Volunteer Management System
Run this script to create all database tables in Supabase
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import create_tables
from app.config import settings

def main():
    """Initialize database tables"""
    print("Initializing database tables...")
    
    try:
        # Check if database configuration is available
        if not settings.database_url and not (settings.supabase_url and settings.supabase_service_role_key):
            print("❌ Error: Database configuration not found!")
            print("Please set up your .env file with Supabase credentials:")
            print("  - SUPABASE_URL")
            print("  - SUPABASE_SERVICE_ROLE_KEY")
            print("  - Or DATABASE_URL")
            return False
        
        # Create tables
        create_tables()
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 