import os
import sys
 
sys.path.insert(0,"/www/lmdb_deploy/www/lmdb_system/lmdb_main")
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'lmdb_main.settings'
 
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
