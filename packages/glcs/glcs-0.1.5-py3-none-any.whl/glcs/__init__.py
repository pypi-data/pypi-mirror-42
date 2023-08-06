# -*- coding: utf-8 -*-
"""Initializer for the glcs package."""
from pathlib import Path
import glcs
import gitlab

NAME = "glcs"
CONFIG_SERVER = "gitlabt"
CONFIG_LOCATION = Path.home() / '.python-gitlab.cfg'
