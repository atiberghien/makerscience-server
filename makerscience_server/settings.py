"""
Django settings for makerscience_server project.

"""
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    ('Alban Tiberghien', 'alban@nonetype.fr'),
)

MANAGERS = ADMINS
# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'dataserver',
        'USER': 'dataserver',
        'PASSWORD': 'dataserver',
    }
}

ALLOWED_HOSTS = ['', '']
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'fr-FR'
LANGUAGES = [
    ('fr-FR', 'French'),
]

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))
MEDIA_ROOT = os.path.join(PROJECT_DIR, '..', 'media/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_DIR, '..', '..', 'static/')
STATIC_URL = '/static/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, '..', 'static/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'afg=tuy3+g+$i*j4#j6x)-u)uvwpf-t0e5ripy+qaw#h^369if'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',

    'corsheaders.middleware.CorsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'makerscience_server.urls'

WSGI_APPLICATION = 'makerscience_server.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, '..', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'sekizai.context_processors.sekizai',
    'multiuploader.context_processors.booleans',
)

# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'grappelli',
    'django.contrib.admin',

    'django_comments',
    'south',
    'corsheaders',
    'reversion',
    'compressor',
    'django_extensions',

    'sekizai',

    'guardian',
    'userena',

    'tastypie',
    'autoslug',
    'taggit',
    'multiuploader',
    'sendfile',
    'sorl.thumbnail',
    'haystack',

    'whoosh',

# From dataserver
    'dataserver',
    'accounts',
    'bucket',
    'scout',

    # 'deal',
    # 'flipflop',
    # 'alambic',
    'projects',
    'projectsheet',
    'graffiti',
    'commons',
    # 'unisson',
    'ucomment',

    'makerscience_catalog',
    'makerscience_profile',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LEAFLET_CONFIG = {
    'TILES_URL': 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'MINIMAP': True,
}

ANONYMOUS_USER_ID = -1
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
#LOGIN_URL = '/login/'
LOGOUT_URL = '/accounts/signout/'

AUTH_PROFILE_MODULE = 'accounts.Profile'



COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
)

# TASTYPIE/API
CORS_ORIGIN_ALLOW_ALL = True
TASTYPIE_FULL_DEBUG = DEBUG
APPEND_SLASH = False
TASTYPIE_ALLOW_MISSING_SLASH=True
TASTYPIE_DEFAULT_FORMATS = ['json']
API_LIMIT_PER_PAGE = 0

# Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'bucket.signals.RelatedRealtimeSignalProcessor'

## bucket
BUCKET_FILES_FOLDER = 'bucket'

## multiuploader
MULTIUPLOADER_FILE_EXPIRATION_TIME = 3600

MULTIUPLOADER_FORMS_SETTINGS = {
    'default': {
        'FILE_TYPES' : ["txt","zip","jpg","jpeg","flv","png"],
        'CONTENT_TYPES' : [
            'image/jpeg',
            'image/png',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/vnd.oasis.opendocument.text',
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.oasis.opendocument.presentation',
            'text/plain',
            'text/rtf',
        ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER':5,
        'AUTO_UPLOAD': True,
    },
}

# SENDFILE
SENDFILE_BACKEND = 'sendfile.backends.development'

# SORL
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine' # Needed for Pdf conv
THUMBNAIL_CONVERT = 'gm convert'

# SOUTH_MIGRATION_MODULES = {
#     'taggit': 'taggit.south_migrations',
# }

#Grappeli
GRAPPELLI_ADMIN_TITLE = "Admin Makerscience"
