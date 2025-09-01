"""AppConfig class for the `locked_migrations` app."""

from django.apps import AppConfig


class LockedMigrationsConfig(AppConfig):
    """Set the name of the app and the default auto field type."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'locked_migrations'
