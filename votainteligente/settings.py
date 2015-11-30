# coding=utf-8
import sys
# Django settings for votainteligente project.
import os

import djcelery
djcelery.setup_loader()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'votainteligente.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Casablanca'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ar' #'fr-fr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

#for I18N et L10N
gettext_noop = lambda x: x

LANGUAGES = (
    ('fr', gettext_noop('French')),
    ('ar', gettext_noop('Arabic')),
)


LOCALE_PATHS = (os.path.join(os.path.dirname(__file__), '../locale/'),)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/" old : 
#the value of media_root is temporaly 
# a solution like upload in CDN as amazon bucket should be implemented.
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'cache')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/cache/'


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2^sj9starkm)(8gk#00aw^ldw(^a72mhwq2v-3_jlw)-+-#%uo'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'elections.middleware.ForceDefaultLanguageMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'flatpages_i18n.middleware.FlatpageFallbackMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'secretballot.middleware.SecretBallotIpMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'votainteligente.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'votainteligente.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "votainteligente.context_processors.get_url_base",
    "votainteligente.context_processors.word_i18n",
    )

TESTING = 'test' in sys.argv
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.flatpages',
    'django_nose',
    'django.contrib.sitemaps',
    'south',
    'taggit',
    'haystack',
    'elections',
    'candideitorg',
    'popit',
    'writeit',
    'markdown_deux',
    'django_extensions',
    'pagination',
    'sorl.thumbnail',
    'django_admin_bootstrapped',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'tinymce',
    'djcelery',
    'secretballot',
    'mptt',
    'modeltranslation',
    'flatpages_i18n',
    'multiupload',
    'extra_views',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

### POPIT DJANGO THINGS THINGS

# Testing related
TEST_POPIT_API_HOST_IP   = '127.0.0.1'
TEST_POPIT_API_PORT      = '3000'
TEST_POPIT_API_SUBDOMAIN = 'popit-django-test'

# create the url to use for testing the database.
# See http://xip.io/ for details on the domain used.
TEST_POPIT_API_URL = "http://%s.%s.xip.io:%s/api" % ( TEST_POPIT_API_SUBDOMAIN,
                                                      TEST_POPIT_API_HOST_IP,
                                                      TEST_POPIT_API_PORT )

POPIT_API_URL = "http://%s.127.0.0.1.xip.io:3000/api"

### POPIT DJANGO THINGS THINGS


### WRITEIT API THINGS

WRITEIT_API_URL = "http://localhost:3001/api/v1/"

WRITEIT_USERNAME = 'admin'
WRITEIT_KEY = 'a'
NEW_ANSWER_ENDPOINT = 'NEW_ANSWER_ENDPOINT'

### WRITEIT API THINGS


### CANDIDEITORG API THINGS

CANDIDEITORG_URL = 'http://localhost:3002/api/v2/'
CANDIDEITORG_USERNAME = 'admin'
CANDIDEITORG_API_KEY = 'a'

### CANDIDEITORG API THINGS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
#CELERY STUFF
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

#django tinyMCE
TINYMCE_JS_URL = os.path.join(STATIC_URL, 'js/tiny_mce/tiny_mce.js')
TINYMCE_JS_ROOT = os.path.join(STATIC_URL, 'js/tiny_mce')
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'width': 500,
    'height': 500,
}
#Django nose
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
if TESTING:

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'votainteligente_test',
        },
    }
else:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'votainteligente',
        },
    }

SOUTH_TESTS_MIGRATE = False
EXTRA_APPS = ()

#navigation bar
# NAV_BAR = ('profiles','questionary','soulmate','facetoface','ask','ranking')
NAV_BAR = ('profiles','questionary','soulmate','facetoface','ask','ranking')
WEBSITE_METADATA = {
    'author' : u'Name of the author',
    'description' : u'A description for the site',
    'keywords' : u'some,tags,separated,by,comma'
}
#for Facebook OGP http://ogp.me/
WEBSITE_OGP = {
    'title' : u'Title page for Facebook OGP',
    'type' : 'website',
    'url' : 'http://nouabook.ma/',
    'image' : 'img/logo1.png'
}
#disqus setting dev
WEBSITE_DISQUS = {
    'enabled' : True,
    'shortname' : 'shortname_disqus',
    'dev_mode' : 0
}
#google analytics
WEBSITE_GA = {
    'code' : 'UA-XXXXX-X',
    'name' : 'ga_name',
    'gsite-verification' : 'BCyMskdezWX8ObDCMsm_1zIQAayxYzEGbLve8MJmxHk'
}
#imgur
WEBSITE_IMGUR = {
    'client_id' : 'eb18642b5b220484864483b8e21386c3' #example client_id, only works with 50 pic a day
}
#settings for global site
WEBSITE_GENERAL_SETTINGS = {
    'home_title' : 'Lorem ipsum dolor sit amet, consectetur adipisicing elit.'
}
#twitter sepparated by comma, eg: votainteligente,votainformado,othertag
WEBSITE_TWITTER = {
    'hashtags' : 'votainteligente'
}
#setting facebook website
WEBSITE_FACEBOOK = {
    'app_id' : 'the_app_id',
    'secret_key' : 'the_secret_key',
    'version' : 'v2.1'
}
USE_POPIT = True
#if you set USE_POPIT to False the USE_WRITEIT param will automatically be interpreted as False
USE_WRITEIT = True
CACHE_MINUTES = 0
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

try:
    from local_settings import *
    INSTALLED_APPS += EXTRA_APPS
except ImportError:
    pass
