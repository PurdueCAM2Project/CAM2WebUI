#!/usr/bin/env python
import os
import sys
import configparser
from pathlib import Path

if __name__ == "__main__":
    # Import variables from .env if the file exists
    parser = configparser.ConfigParser({k: v.replace('$', '$$') for k, v in os.environ.items()},
             interpolation=configparser.ExtendedInterpolation())
    def defaultSect(fp): yield '[DEFAULT]\n'; yield from fp
    settingsFile = Path(__file__).parent.resolve() / ".env"
    if settingsFile.is_file():
        with open(settingsFile) as stream:
            parser.read_file(defaultSect(stream))
            for k, v in parser["DEFAULT"].items():
                os.environ.setdefault(k, v)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cam2webui.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
