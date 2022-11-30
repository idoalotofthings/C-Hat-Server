#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json
import importlib
from busprovider import bus
from eventbus.event import Event

def main():

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'c_hat_server.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    register_events()
    load_plugins()
    
    bus.start()

    execute_from_command_line(sys.argv)
    

def register_events():
    for event in Event:
        bus.register_event(event)

def load_plugins():
    try:
        plugins = json.load(open("plugins.json"))
        for plugin in plugins:
            importlib.import_module(f"plugins.{plugin}.{plugin}")
            print(f"Loaded {plugin}")
    except Exception as e:
        print("Error loading plugins:", e)

if __name__ == '__main__':
    main()
