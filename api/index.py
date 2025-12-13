import os
import sys

from django.core.wsgi import get_wsgi_application

# Add project path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jobBoard.settings")

application = get_wsgi_application()
