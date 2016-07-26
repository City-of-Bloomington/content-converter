import os, sys, re
sys.path.append(os.path.dirname(os.getcwd()))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "converter.settings")

import django
django.setup()

from pages.models import Page

print Page.objects.all()
