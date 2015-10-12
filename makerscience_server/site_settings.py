# -*- coding: utf-8 -*-

import os
import dj_database_url


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alban Tiberghien', 'alban@nonetype.fr'),
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*', ]

DATABASES = {
    'default':
        dj_database_url.parse(
            os.environ.get(
                'UNISSON_DATA_SERVER_DATABASE',

                # default value for database is `dataserver` × 3
                'postgis://dataserver:dataserver@localhost/dataserver')
        )
}

# Haystack (for bucket module)
HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        # 'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
        # 'INDEX_NAME': 'bucket',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'bucket.signals.RelatedRealtimeSignalProcessor'

AUTHENTICATED_USERS_PERMISSIONS = (
    'accounts.add_objectprofilelink',
    'accounts.change_objectprofilelink',
    'accounts.delete_objectprofilelink',
    'accounts.change_profile',
    'accounts.view_profile',
    'bucket.add_bucket',
    'bucket.change_bucket',
    'bucket.view_bucket',
    'bucket.add_bucketfile',
    'bucket.delete_bucketfile',
    'django_comments.add_comment',
    'django_comments.change_comment',
    'django_comments.delete_comment',
    'django_comments.add_commentflag',
    'django_comments.change_commentflag',
    'projects.add_project',
    'projects.change_project',
    'projects.add_projectprogress',
    'projects.change_projectprogress',
    'projects.delete_projectprogress',
    'projects.add_projectprogressrange',
    'projects.change_projectprogressrange',
    'projects.delete_projectprogressrange',
    'projectsheet.add_projectsheet',
    'projectsheet.change_projectsheet',
    'projectsheet.add_projectsheetquestion',
    'projectsheet.change_projectsheetquestion',
    'projectsheet.add_projectsheetquestionanswer',
    'projectsheet.change_projectsheetquestionanswer',
    'scout.add_place',
    'scout.change_place',
    'scout.add_postaladdress',
    'scout.change_postaladdress',
    'taggit.add_tag',
    'taggit.change_tag',
    'taggit.delete_tag',
    'taggit.add_taggeditem',
    'taggit.change_taggeditem',
    'taggit.delete_taggeditem',
    'megafon.add_post',
    'megafon.change_post',
    'megafon.delete_post',
    'starlet.add_vote',
    'starlet.change_vote',
    'starlet.delete_vote',
)

MS_AUTHENTICATED_USERS_PERMISSIONS = (
    'makerscience_catalog.add_makerscienceproject',
    'makerscience_catalog.add_makerscienceresource',
    'makerscience_catalog.add_makerscienceprojecttaggeditem',
    'makerscience_catalog.change_makerscienceprojecttaggeditem',
    'makerscience_catalog.delete_makerscienceprojecttaggeditem',
    'makerscience_catalog.add_makerscienceresourcetaggeditem',
    'makerscience_catalog.change_makerscienceresourcetaggeditem',
    'makerscience_catalog.delete_makerscienceresourcetaggeditem',

    'makerscience_profile.add_makerscienceprofiletaggeditem',
    'makerscience_profile.change_makerscienceprofiletaggeditem',
    'makerscience_profile.delete_makerscienceprofiletaggeditem',

    'makerscience_forum.change_makersciencepost',
    'makerscience_forum.add_makersciencepost',
    'makerscience_forum.change_makersciencepost',
    'makerscience_forum.delete_makersciencepost',

    'notifications.change_notification',
)

API_LIMIT_PER_PAGE = 0

PAGEVIEWS_FILTER = (
    'makerscience/post',
)

OBJECTPROFILELINK_CHOICES = (
    (0, "A rejoint l'équipe du projet"),
    (1, 'Apporte son aide au projet'),
    (2, 'Suit le projet'),
    (3, 'Commentateur du projet'),
    (4, 'A noté le projet'),
    (5, "A invité à rejoindre l'équipe du projet"),
    (6, "A invité à aider le projet"),
    (7, "A ajouté une news"),

    (10, "Auteur de l'expérience"),
    (11, "A une expérience similiaire"),
    (12, "Fan de l'expérience"),
    (13, "Commentateur d'expérience"),
    (14, "A noté pour l'expérience"),
    (15, "A invité à rejoindre les co-auteurs"),
    (16, "A invité à partager son expérience similaires"),

    (30, 'Auteur de la discussion'),
    (31, 'Contributeur à la discussions'),
    (32, 'Suiveur de la discussion'),
    (33, 'Fan de la discussion'),
    (34, "Fan d'une réponse à la discussion"),

    (40, 'Contact'),
    (41, 'A mentionné'),

    (50, 'A taggé'),
    (51, 'Suit un tag'),
)


GOOGLE_CLIENT_ID = "255067193649-5s7fan8nsch2cqft32fka9n36jcd37qg.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "cBbOGD00G7vJKtZRVRbgZjp1"

GOOGLE_RECAPTCHA_SECRET = "6LfrjQwTAAAAAETHPjmsU1IpkyZLBH-nkSyFMNup"

FACEBOOK_CLIENT_ID = "724284684343376"
FACEBOOK_CLIENT_SECRET = "c52b4201756a5da6f6808a5c9e1f5a98"

TWITTER_CLIENT_ID = "RXz5fy5X4M1LewAeNliME2gbM"
TWITTER_CLIENT_SECRET = "nCz6RzDXYJAfxDw5ZNJx9ZMw1dg5RK5jDt3fr9imLqtLNtXSjx"

CORS_ORIGIN_WHITELIST = (
        'localhost:8001',
        '127.0.0.1:8001',
        '127.0.0.1:8002',
        'https://api.twitter.com',
        'http://localhost:8001',
        'makerscience.nonetype.net'
)

MEDIA_URL = '/media/'

VOTE_TYPE_CHOICES = (
    ("makerscienceproject_vote_1", "Original"),
    ("makerscienceproject_vote_2", "Fun"),
    ("makerscienceproject_vote_3", "Prometteur"),
    ("makerscienceresource_vote_1", "Inspirant"),
    ("makerscienceresource_vote_2", "Récomfortant"),
    ("makerscienceresource_vote_3", "Utile"),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}

USERENA_MUGSHOT_SIZE = 150

EMAIL_HOST = 'smtp.gmail.com'
MAKERSCIENCE_BASE_URL = "CHANGE_ME"
EMAIL_PORT = 587
# EMAIL_HOST_PASSWORD = 'thepassword'
EMAIL_HOST_USER = 'makerscience@gmail.com'
EMAIL_USE_TLS = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
RESET_PASSWORD_URL = 'http://data.nonetype.fr/reset/password' #without trailing slash
AES_KEY =  'CHANGE_ME'
AES_IV = 'CHANGE_ME'
