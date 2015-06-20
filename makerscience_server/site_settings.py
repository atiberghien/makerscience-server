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
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        'INDEX_NAME': 'bucket',
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
    )
