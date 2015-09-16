import os
import sys
import site

ENV_PATH = "/home/www/makerscience.fr/server"
APP_NAME = "makerscience-server"
MAIN_MODULE = "makerscience_server"

site.addsitedir('%s/lib/python2.7/site-packages' % ENV_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings" % MAIN_MODULE)

sys.path.append('%s/%s/%s' % (ENV_PATH, APP_NAME, MAIN_MODULE))
sys.path.append('%s/%s' % (ENV_PATH, APP_NAME))

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
