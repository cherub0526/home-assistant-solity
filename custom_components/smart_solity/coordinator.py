"""DataUpdateCoordinator for the smart_solity integration."""

from typing import override

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    SmartSolityApiClient,
    SmartSolityApiError,
    SmartSolityAuthError,
    SmartSolityConnectionError,
    SmartSolityDevice,
    SmartSolityStatus,
)
from .const import DOMAIN, LOGGER, UPDATE_INTERVAL

type SmartSolityConfigEntry = ConfigEntry[SmartSolityDataUpdateCoordinator]


class SmartSolityDataUpdateCoordinator(DataUpdateCoordinator[SmartSolityStatus]):
    """Coordinator that polls the smart_solity lock status."""

    config_entry: SmartSolityConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: SmartSolityConfigEntry,
        api: SmartSolityApiClient,
        device: SmartSolityDevice,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self.api = api
        self.device = device

    @override
    async def _async_update_data(self) -> SmartSolityStatus:
        """Fetch the latest lock status."""
        try:
            return await self.api.get_status(self.device.device_id)
        except SmartSolityAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except (SmartSolityApiError, SmartSolityConnectionError) as err:
            raise UpdateFailed(str(err)) from err
