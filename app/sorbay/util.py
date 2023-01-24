from django.conf import settings

from settings.constants import ENVS


def is_on_dev_environment():
    """Are we currently on the DEV environment?"""
    return settings.ENV == ENVS.DEV


def is_on_production_environment():
    """Are we currently on the PROD environment?"""
    return settings.ENV == ENVS.PRODUCTION
