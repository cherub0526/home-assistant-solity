"""Constants for the smart_solity integration."""

from datetime import timedelta
import logging

DOMAIN = "smart_solity"
MANUFACTURER = "Solity"
LOGGER = logging.getLogger(__package__)
UPDATE_INTERVAL = timedelta(seconds=30)
