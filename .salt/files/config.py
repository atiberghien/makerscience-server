#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (print_function,
                        division,
                        absolute_import)
__docformat__ = 'restructuredtext en'
{%- set cfg = salt['mc_project.get_configuration'](cfg) %}
{%- set data = cfg.data %}

{%- macro render_setting(setting, value=None) %}
{%- set setting = setting.strip() %}
{%- if setting == 'ALLOWED_HOSTS' %}
{%-    for i in data.server_aliases %}
{%-      if i not in value %}
{%-         do value.append(i) %}
{%-      endif %}
{%-    endfor %}
{%- endif %}

{% if setting == 'ADMINS' %}
ADMINS = (
    {% for dadmins in data.admins -%}
    {% for admin, adata in dadmins.items() -%}
    ('{{admin}}', '{{adata.mail}}'),{# jinja indentation whitespace-#}
    {% endfor %}
    {% endfor %}
)
{% elif setting in [
    'LANGUAGES',
    'ADDITIONAL_TEMPLATE_DIRS',
] %}
{{setting}} = (
{%  for v in value -%}
        {{v-}},
{% endfor %}
)
{% elif salt['mc_utils.is_a_set'](value)
      or salt['mc_utils.is_a_list'](value)
      or salt['mc_utils.is_a_dict'](value) %}
try:
    {{setting}} = json.loads("""{{salt['mc_utils.json_dump'](value, pretty=True)}}""".strip())
except ValueError:
    try:
        {{setting}} = json.loads("""{{salt['mc_utils.json_dump'](value)}}""".strip())
    except ValueError:
        {{setting}} = json.loads("""{{salt['mc_utils.json_dump'](value)}}""".replace('\n', '\\n').strip())
{% elif (
    salt['mc_utils.is_a_bool'](value)
    or salt['mc_utils.is_a_number'](value)
)%}
{{-setting}} = {{value}}
{% elif salt['mc_utils.is_a_str'](value) %}
{{-setting}} = """{{value}}"""
{% else %}
{{-setting}} = {{value}}
{%- endif %}
{%- endmacro %}

import json
from django.utils.translation import gettext_lazy as _
{% for setting, value in data.get('django_settings', {}).items() -%}
{{render_setting(setting, value)}}
{%- endfor %}
{% for setting, value in data.get('extra_django_settings', {}).items() -%}
{{render_setting(setting, value)}}
{%- endfor %}
{% for setting, value in data.get('extra_settings', {}).items() %}
{{setting}} = {{value}}
{% endfor %}

VOTE_TYPE_CHOICES = (
    ("makerscienceproject_vote_1", "Original"),
    ("makerscienceproject_vote_2", "Fun"),
    ("makerscienceproject_vote_3", "Prometteur"),
    ("makerscienceresource_vote_1", "Inspirant"),
    ("makerscienceresource_vote_2", "Réconfortant"),
    ("makerscienceresource_vote_3", "Utile"),
)
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
    'projects.change_projectnews',
    'projects.delete_projectnews',
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
PAGEVIEWS_FILTER = (
    'makerscience/post',
)
API_LIMIT_PER_PAGE = 0

OBJECTPROFILELINK_CHOICES = (
    (0, "membre de l'équipe du projet"),
    (1, 'apporte son aide au projet'),
    (2, 'suit le projet'),
    (3, 'commentateur du projet'),
    (4, 'notation du projet'),
    (5, "invitation à rejoindre l'équipe du projet"),
    (6, "invitation à aider le projet"),
    (7, "auteur d'un une news"),

    (9, "auteur d'une des ressources"),
    (10, "contributeur de la ressource"),
    (11, "a une expérience similiaire"),
    (12, "suit la ressource"),
    (13, "commentateur de la ressource"),
    (14, "notation de la ressource"),
    (15, "invitation à devenir auteur"),
    (16, "invitation à partager son expérience similaires"),

    (30, 'auteur du post'),
    (31, 'contributeur à la discussions'),
    (32, 'suit la discussion'),
    (33, 'aime la discussion'),
    (34, "aime une réponse à la discussion"),

    (40, 'suit le membre'),
    (41, 'a mentionné'),

    (50, 'a taggé'),
    (51, 'suit un tag'),
)
USERENA_MUGSHOT_SIZE = 150

# vim:set et sts=4 ts=4 tw=80:
