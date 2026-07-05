"""Lock platform for the smart_solity integration."""

from typing import Any, override

from homeassistant.components.lock import LockEntity
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .api import SmartSolityApiError, SmartSolityConnectionError
from .coordinator import SmartSolityConfigEntry, SmartSolityDataUpdateCoordinator
from .entity import SmartSolityEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: SmartSolityConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the smart_solity lock entity."""
    async_add_entities([SmartSolityLock(config_entry.runtime_data)])


class SmartSolityLock(SmartSolityEntity, LockEntity):
    """Representation of a smart_solity lock."""

    _attr_name = None

    def __init__(self, coordinator: SmartSolityDataUpdateCoordinator) -> None:
        """Initialize the lock."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.device.device_id

    @property
    @override
    def is_locked(self) -> bool:
        """Return true if the lock is locked."""
        return self.coordinator.data.is_locked

    @override
    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the device."""
        try:
            await self.coordinator.api.lock(self.coordinator.device.device_id)
        except (SmartSolityApiError, SmartSolityConnectionError) as err:
            raise HomeAssistantError(str(err)) from err
        await self.coordinator.async_request_refresh()

    @override
    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the device."""
        try:
            await self.coordinator.api.unlock(self.coordinator.device.device_id)
        except (SmartSolityApiError, SmartSolityConnectionError) as err:
            raise HomeAssistantError(str(err)) from err
        await self.coordinator.async_request_refresh()
