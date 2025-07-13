from configparser import ConfigParser
import os
import ast
from pathlib import Path

""""
--------------
SETTINGS
--------------
"""

ROOT_PATH=Path(__file__).parent.absolute()
config=ConfigParser(interpolation=None)
config_file_path = ROOT_PATH / "config.ini"
config.read(config_file_path)
api_creds = config["RingCentral"]
