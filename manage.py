#!/usr/bin/env python
import os
import sys
import glob
import re


def read_envdir():
    """
    Reads environment variables from env directory and
    sets them as default values to os.environ.

    This is practically only used in development, in production
    envdir is used to load the env variables before running
    any commands!
    """
    env_dir = "env"
    env_vars = glob.glob(os.path.join(env_dir, '*'))
    for env_var in env_vars:
        with open(env_var, 'r') as env_var_file:
            os.environ.setdefault(env_var.split(os.sep)[-1],
                                  env_var_file.read().strip())


if __name__ == "__main__":
    read_envdir()

    # If no settings spesified, load development settings.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dotmembership.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
