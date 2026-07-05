"""Sensor platform for the smart_solity integration."""

from typing import override

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import SmartSolityConfigEntry, SmartSolityDataUpdateCoordinator
from .entity import SmartSolityEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: SmartSolityConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the smart_solity battery sensor."""
    async_add_entities([SmartSolityBatterySensor(config_entry.runtime_data)])


class SmartSolityBatterySensor(SmartSolityEntity, SensorEntity):
    """Battery sensor for a smart_solity lock."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator: SmartSolityDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device.device_id}_battery"

    @property
    @override
    def native_value(self) -> int:
        """Return the battery percentage."""
        return self.coordinator.data.battery
