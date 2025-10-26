"""
Django settings for messaging_app project - Test configuration

This settings file is used specifically for running tests with MySQL database.
It inherits from the base settings and overrides the database configuration.
"""
import os
from .settings import *  # noqa: F401, F403

# Override database configuration for tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', 'messaging_test'),
        'USER': os.environ.get('MYSQL_USER', 'testuser'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'testpass'),
        'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'TEST': {
            'NAME': 'messaging_test',
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci',
        },
    }
}

# Disable migrations during tests for faster execution
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

# Uncomment the line below to disable migrations in tests
# MIGRATION_MODULES = DisableMigrations()

# Test-specific settings
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
USE_TZ = True

# Speed up password hashing during tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable logging during tests
LOGGING_CONFIG = None

