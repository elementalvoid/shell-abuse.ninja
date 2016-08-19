#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Matt Klich - Chief Abuser'
SITENAME = u'Shell Abuse'
SITESUBTITLE = u'Bending the shell to your whim - occasionally with abandon.'
SITEURL = 'http://localhost:8000'

PATH = 'content'

TIMEZONE = 'America/Denver'

DEFAULT_LANG = u'en'

FEED_DOMAIN = SITEURL
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Theme and theme config
THEME = "Flex"
SITELOGO = "/images/elementalvoid-avatar.png"
DISQUS_SITENAME = "shellabuse"
MAIN_MENU = True
USE_FOLDER_AS_CATEGORY = True
MENUITEMS = (
    ('Archives', '/archives.html'),
    ('Categories', '/categories.html'),
    ('Tags', '/tags.html'),
)
PYGMENTS_STYLE = 'github'
BROWSER_COLOR = '#333'
# End theme and theme config

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2}T\d{2}:\d{2})_(?P<slug>.*)'

STATIC_PATHS = ['images', 'extra/CNAME']
EXTRA_PATH_METADATA = {
    'images/favicon.ico': {'path': 'favicon.ico'},
    'extra/CNAME': {'path': 'CNAME'},
}

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['related_posts', 'sitemap', 'post_stats']
# End Plugins

TYPOGRIFY = True

# Blogroll
# LINKS = (
#     ('Pelican', 'http://getpelican.com/'),
#     ('Python.org', 'http://python.org/'),
#     ('Jinja2', 'http://jinja.pocoo.org/'),
# )


# Social widget
SOCIAL = (
    ('linkedin', 'https://www.linkedin.com/in/mattklich'),
    ('github', 'https://github.com/elementalvoid'),
    ('stack-overflow', 'http://stackoverflow.com/users/436190/elementalvoid'),
    ('google', 'https://google.com/+MattKlich'),
    ('rss', '//shell-abuse.ninja/feeds/all.atom.xml')
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
