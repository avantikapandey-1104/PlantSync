#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    print("✅ manage.py loaded successfully")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PlantSync.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        print("❌ Django Import Error")
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    print("🚀 Starting Django runserver command")
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
