# Django settings for the basic OpenHatch 'mysite' project

## Imports
import os
import logging
import datetime
import sys
import dj_database_url

## Figure out where in the filesystem we are.
DIRECTORY_CONTAINING_SETTINGS_PY = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT_BEFORE_STATIC = DIRECTORY_CONTAINING_SETTINGS_PY # This is needed for {% version %}

GITHUB_USERNAME_BASE_PATH = 'https://github.com'
GOOGLE_CODE_USERNAME_BASE_PATH = 'https://code.google.com/u'

## Now, actual settings
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Asheesh Laroia', 'asheesh@openhatch.org'),
)

MANAGERS = ADMINS

DATABASE_OPTIONS = {
    'read_default_file': './my.cnf',
}

TEST_DATABASE_OPTIONS = {
    'read_default_file': './my.cnf',
}

DATABASE_CHARSET = 'utf8'           # omg I hate you MySQL
TEST_DATABASE_CHARSET = 'utf8'      # have to apply it to the test database, too

DATABASES = {
    'default': {
        'NAME': os.path.join(MEDIA_ROOT_BEFORE_STATIC, 'site.db'),
        'ENGINE': 'django.db.backends.sqlite3',
        'CHARSET': 'utf8',
    },
}

# Permit it to be overriden
if 'DATABASE_URL' in os.environ:
    DATABASES = {'default': dj_database_url.config()}

OTHER_DATABASES = {
    'mysql': {
        'NAME': 'oh_milestone_a',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': 'oh_milestone_a',
        'PASSWORD': 'ahmaC0Th',
        'OPTIONS': {'read_default_file': os.path.join(os.path.dirname(__file__), 'my.cnf')},
        'CHARSET': 'utf8',
    },
}

if os.environ.get('USE_MYSQL', ''):
    DATABASES['default'] = OTHER_DATABASES['mysql']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(MEDIA_ROOT_BEFORE_STATIC, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'k%&pic%c5%6$%(h&eynhgwhibe9-h!_iq&(@ktx#@1-5g2+he)'

TEMPLATE_CONTEXT_PROCESSORS = (
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.debug',
            'django.core.context_processors.i18n',
            'django.core.context_processors.media',
            'django.core.context_processors.request',
            'django_authopenid.context_processors.authopenid',
        )

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = [
    'mysite.base.middleware.DetectLogin', # This must live on top of Auth + Session middleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'mysite.base.middleware.StaticGeneratorMiddlewareOnlyWhenAnonymous',
    'sessionprofile.middleware.SessionProfileMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'mysite.base.middleware.HandleWannaHelpQueue',
    'django.middleware.transaction.TransactionMiddleware',
    # Django debug toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

)

STATIC_GENERATOR_URLS = (
    r'^/people/',
    r'^/search/',
    r'^/\+cacheable/',
)

STATIC_DOC_ROOT = 'static/'

# Sessions in /tmp
# mysite.account.view_helpers.clear_user_sessions assumes the DB backend, it
# will not work otherwise
SESSION_ENGINE="django.contrib.sessions.backends.db"

INSTALLED_APPS = (
    'ghettoq',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.webdesign',
    'django.contrib.admin',
    'registration',
    'django_authopenid',
    'django_extensions',
    'south',
    'django_assets',
    'file_resubmit',
    'celery',
    'invitation',
    'mysite.search',
    'mysite.profile',
    'mysite.customs',
    'mysite.account',
    'mysite.base',
    'mysite.project',
    'voting',
    'reversion',
    'debug_toolbar',
    'sessionprofile',
    'model_utils',
    'djcelery',
    'djkombu',
    'django_crontab',
    'corsheaders',
    'tinymce'
)

CORS_ORIGIN_ALLOW_ALL = True

# testrunner allows us to control which testrunner to use
TEST_RUNNER = 'mysite.testrunner.OpenHatchTestRunner'
# Optionally, use XML reporting
if os.environ.get('USE_XML_TEST_REPORTING', None):
    TEST_RUNNER = 'mysite.testrunner.OpenHatchXMLTestRunner'

# Make test names prettier
TEST_OUTPUT_DESCRIPTIONS = True

TEST_OUTPUT_DIR = "test_output"

## AMQP, Rabbit Queue, Celery
BROKER_BACKEND='django'

cooked_data_password = 'AXQaTjp3'
AUTH_PROFILE_MODULE = "profile.Person"

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/' # Landing page

OHLOH_API_KEY='JeXHeaQhjXewhdktn4nUw' # This key is called "Oman testing"
                                        # at <https://www.ohloh.net/accounts/paulproteus/api_keys>
#OHLOH_API_KEY='0cWqe4uPw7b8Q5337ybPQ' # This key is called "API testing"

logging.basicConfig(
    level = logging.ERROR,
    format = '%(asctime)s %(funcName)s:%(lineno)d %(levelname)-8s %(message)s',
)

# Invite codes last seven days
ACCOUNT_INVITATION_DAYS=7
INVITE_MODE=False # Enable this on production site ...?
INVITATIONS_PER_USER=100

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'openhatch'
    },
    "file_resubmit": {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        "LOCATION": '/tmp/file_resubmit/'
    }
}

# Launchpad credentials
LP_CREDS_BASE64_ENCODED='WzFdCmNvbnN1bWVyX3NlY3JldCA9IAphY2Nlc3NfdG9rZW4gPSBHV0tKMGtwYmNQTkJXOHRQMWR2Ygpjb25zdW1lcl9rZXkgPSBvcGVuaGF0Y2ggbGl2ZSBzaXRlCmFjY2Vzc19zZWNyZXQgPSBSNWtrcXBmUERiUjRiWFFQWGJIMkdoc3ZQamw2SjlOc1ZwMzViN0g2d3RjME56Q3R2Z3JKeGhNOVc5a2swU25CSnRHV1hYckdrOFFaMHZwSgoK'

GITHUB_USERNAME='paulproteus'
GITHUB_API_TOKEN='ceb85898146b6a0d4283cdf8788d8b6a'

# How ASSETS_DEBUG works
# Value     Effect
#   True        Don't pack assets in DEBUG mode
#   False       Pack assets in DEBUG mode
ASSETS_DEBUG = False

ADD_VERSION_STRING_TO_IMAGES = True
ADD_VERSION_STRING_TO_IMAGES_IN_DEBUG_MODE = True

# The setting below adds a querystring to assets, e.g. bundle.css?1264015076
# This querystring changes whenever we change the asset. This prevents the
# client's cached version of an asset from overriding our new asset.
ASSETS_EXPIRE = 'querystring'
WHAT_SORT_OF_IMAGE_CACHE_BUSTING = ASSETS_EXPIRE

INTERNAL_IPS = ('127.0.0.1',)

FORWARDER_DOMAIN = "forwarder.openhatch.org"
FORWARDER_LISTINGTIME_TIMEDELTA = datetime.timedelta(days=2) # how long the forwarder is listed
FORWARDER_LIFETIME_TIMEDELTA = datetime.timedelta(days=5) # how long the forwarder actually works
# note about the above: for 3 days, 2 forwarders for the same user work.
# at worst, you visit someone's profile and find a forwarder that works for 3 more days
# at best, you visit someone's profile and find a forwarder that works for 5 more days
# at worst, we run a postfixifying celery job once every two days for each user

POSTFIX_FORWARDER_TABLE_PATH = None # Disabled by default

CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

#CELERY_ALWAYS_EAGER = True # This is set to True in the test runner also.

WEB_ROOT = os.path.join(MEDIA_ROOT, '_cache')

SERVER_NAME='openhatch.org'

# The script to invoke for management commands in this environment.
PATH_TO_MANAGEMENT_SCRIPT = os.path.abspath(os.path.join(DIRECTORY_CONTAINING_SETTINGS_PY, '../manage.py'))
CELERY_ALWAYS_EAGER = True
SOUTH_TESTS_MIGRATE = False


# This setting is used by the customs bug importers.
TRACKER_POLL_INTERVAL = 1  # Days

### Initialize celery
import djcelery
djcelery.setup_loader()

# By default, Django logs all SQL queries to stderr when DEBUG=True. This turns
# that off.  If you want to see all SQL queries (e.g., when running a
# management command locally), remove the stanza related to django.db.backends.
#
# Also, this setup sends an email to the site admins on every HTTP 500 error
# when DEBUG=False.
#
# The lines relating to 'require_debug_false' should be enabled when the
# project is upgraded to use Django 1.4.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'ERROR',
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['null'], # Quiet by default!
            'propagate': False,
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DOWNLOADED_GEOLITECITY_PATH = os.path.join(MEDIA_ROOT,
                                           '../../downloads/GeoLiteCity.dat')

### Heroku fix-ups
### If we are running on Heroku, there will be a DATABASE_URL
### and/or SHARED_DATABASE_URL that refers to postgres.
### Our South migrations do not currently run on postgres, so
### in that case, we skip south.
_overridden_db = (os.environ.get('DATABASE_URL', '') or
                  os.environ.get('SHARED_DATABASE_URL', ''))
if _overridden_db.startswith('postgres://'):
    INSTALLED_APPS = tuple([x for x in INSTALLED_APPS
                            if x != 'south'])

### Windows fix-ups
if sys.platform.startswith('win'):
    # staticgenerator seems to act weirdly on Windows, so we disable it.
    MIDDLEWARE_CLASSES.remove(
        'mysite.base.middleware.StaticGeneratorMiddlewareOnlyWhenAnonymous')

### Enable the low-quality, high-load bug recommendation system
RECOMMEND_BUGS=True

ENABLE_NEW_IWH_HANDLER = False

### SocialCoding4Good

CRONTAB_DJANGO_MANAGE_PATH = PATH_TO_MANAGEMENT_SCRIPT

CRONJOBS = [
    ('@daily', 'mysite.cron.push_volunteers_to_zoho_crm')
]

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'cleanup_on_startup': True,
    'height': 500,
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,"
                                "|,formatselect,|,hr,removeformat,visualaid,|,sub,sup,|,charmap",
	'theme_advanced_buttons2' : "bullist,numlist,|,outdent,indent,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code",
    'theme_advanced_buttons3' : "",
    'forced_root_block' : 'div',
}

### Include a user's customizations
try:
    from local_settings import *
except ImportError:
    pass

try:
    import bugimporters
except ImportError:
    try:
        sys.path.append(os.path.join('..', 'oh-bugimporters'))
        import bugimporters
    except ImportError:
        # meh.
        pass
