import os, sys
sys.path.append('/home/gbtux/Projets/Django/forjme')

os.environ['DJANGO_SETTINGS_MODULE'] = 'forjme.settings'
import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
