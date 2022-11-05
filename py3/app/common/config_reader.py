"""Reads the config json file"""

from collections import namedtuple
from json import load
from pathlib import Path


def get_conf(json_file="config"):
    """Returns the configuration from the config file
    Args: json_file (str, optional): Name of the config file (without file type). Defaults to "config".
    """
    with open(Path(Path(__file__).parent.absolute(), f"{json_file}.json"), "r") as conf:
        return load(conf, object_hook=lambda d: namedtuple("conf", d.keys())(*d.values()))
