import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Justyna Ilczuk', 'justyna.ilczuk@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'retro',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'retro',
        'PASSWORD': 'retro',
        'HOST': 'retro',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': 'retro',                      # Set to empty string for default.
    }
}

ALLOWED_HOSTS = []


LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

PATH_PROJECT = PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
#"/home/att/projects/retrospective/retrospective/"

STATIC_ROOT = PATH_PROJECT
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
   PATH_PROJECT + 'static/css',
   PATH_PROJECT + 'static',
)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'cp6!p_9k(1ft(og*vf5xbn7_$$@%)f9n!we=dad0muc353f4*e'

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
)

ROOT_URLCONF = 'retrospective.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'retrospective.wsgi.application'

TEMPLATE_DIRS = (
    PATH_PROJECT + '/templates/',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

    
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'core',
    'django_extensions',
    'django_crontab',
    'south',
    'django.contrib.admindocs',
    'registration',
    'mailing',
    'rest_framework',
)

CRONJOBS = [
    ('0 0 * * *', 'retrospective.mailing.send_mails.send_mails')
]

ACCOUNT_ACTIVATION_DAYS = 7

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

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
    ]
}