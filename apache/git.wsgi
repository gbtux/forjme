import os, sys
import logging

logger = logging.getLogger('dashboard')
sys.path.append('/home/gbtux/Projets/Django/forjme')

os.environ['DJANGO_SETTINGS_MODULE'] = 'forjme.settings'

from django.contrib.auth.models import User
from django import db
from dashboard.models import Project

def check_password(environ, user, password):
    db.reset_queries() 

    kwargs = {'username': user, 'is_active': True} 

    try: 
        try: 
            user = User.objects.get(**kwargs)
	    logger.debug('user : %s' % user) 
        except User.DoesNotExist: 
            return None

        if user.check_password(password):
	    logger.debug('check password OK') 
            return True
        else: 
	    logger.debug('check password KO') 
            return False
    finally: 
        db.connection.close() 
