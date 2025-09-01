import os
import sys

project_home = '/home/yourusername/COPO'
if project_home not in sys.path:
    sys.path.append(project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'copos.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
