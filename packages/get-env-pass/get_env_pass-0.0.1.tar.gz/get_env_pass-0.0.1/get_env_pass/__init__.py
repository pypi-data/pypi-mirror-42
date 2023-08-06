"""
Contains utils and functions for python-getenvpass module
"""
from getpass import getpass
import os


def get_env_pass(env_var=''):
    """
    Retrieves environment variable. If does not exist, run getpass module

    Returns:
        Environment variable value or getpass.

    """
    return os.environ[env_var] if env_var in os.environ else getpass()
