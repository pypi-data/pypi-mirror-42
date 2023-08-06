"""
it4ifree portal clients config
"""

import ConfigParser
import os
import sys
import re

from .logger import LOGGER

DEFAULT_CONFIG_PATH = '/usr/local/etc/it4i-portal-clients/main.cfg'
LOCAL_CONFIG_PATH = os.path.expanduser('~/.it4ifree')

CONFIG = ConfigParser.ConfigParser()
CONFIG_FILES = '\n'.join((4*' ' + DEFAULT_CONFIG_PATH,
                          4*' ' + LOCAL_CONFIG_PATH))

try:
    CONFIG.readfp(open(DEFAULT_CONFIG_PATH))
except IOError:
    LOGGER.warning("Default config file %s not found", DEFAULT_CONFIG_PATH)
    if not CONFIG.read(LOCAL_CONFIG_PATH):
        LOGGER.error("Tried (in the following order), but no configuration found:\n%s",
                     CONFIG_FILES)
        sys.exit(1)

if not CONFIG.read(LOCAL_CONFIG_PATH):
    LOGGER.info("Local config file %s not found", LOCAL_CONFIG_PATH)

# mandatory configuration options
API_URL = "https://scs.it4i.cz/api/v1/"
API_URL_OPTNAME = "api_url"
try:
    API_URL = CONFIG.get("main", API_URL_OPTNAME)
except BaseException:
    pass

API_URL = re.sub(r'\/$', '', API_URL)

IT4IFREETOKEN = None
IT4IFREETOKEN_OPTNAME = "it4ifreetoken"
try:
    IT4IFREETOKEN = CONFIG.get("main", IT4IFREETOKEN_OPTNAME)
except BaseException:
    LOGGER.error("""Missing or unset configuration option: %s

Suggested paths:
%s
""", IT4IFREETOKEN_OPTNAME, CONFIG_FILES)
    sys.exit(1)
