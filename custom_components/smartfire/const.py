"""Constants for the Smartfire integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "smartfire"

# Configuration keys
CONF_BASE_URL = "base_url"
CONF_INSTALL_TYPE = "install_type"
CONF_HOST = "host"
CONF_PORT = "port"

# Install types
INSTALL_TYPE_LOCAL = "local"
INSTALL_TYPE_REMOTE = "remote"

# API defaults
DEFAULT_PORT = 5000
DEFAULT_LOCAL_URL = "http://127.0.0.1:5000"
