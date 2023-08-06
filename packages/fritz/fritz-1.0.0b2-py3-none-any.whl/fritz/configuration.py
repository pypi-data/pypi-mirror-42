"""
fritz.configuration
~~~~~~~~~~~~~~~~~~~

Helps manage fritz configuration.

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""

import os
from pathlib import Path
import configparser

import fritz
import fritz.errors


_HOME = str(Path.home())
CONFIG_PATH = os.path.join(_HOME, ".fritz")


def init_config(path=CONFIG_PATH):
    """Initializes Fritz configuration, by default checking ~/.fritz.

    Args:
        path (str): Set path to override where config file is initialized from.
    """
    fritz_config = load_config_file(path=path)
    try:
        defaults = dict(fritz_config.items("default"))
        fritz.configure(
            api_key=defaults["api_key"],
            project_uid=defaults["project_uid"],
            api_base=defaults.get("api_base"),
        )
    except (configparser.NoSectionError, KeyError):
        raise fritz.errors.InvalidFritzConfigError(path)


def load_config_file(path=CONFIG_PATH):
    """Loads configuration file from disk.

    Args:
        path (str): Path of config file to load.

    Returns: ConfigParser
    """
    fritz_config = configparser.ConfigParser()
    fritz_config.read(path)
    return fritz_config


def write_config_file(fritz_config, path=CONFIG_PATH):
    """Writes provide configuration file.

    Args:
        fritz_config (ConfigParser): Configuration to save.
        path (str): Path of destination config file.
    """
    fritz_config.write(open(path, "w"))
