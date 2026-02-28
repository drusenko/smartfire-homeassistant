"""Switch platform for Smartfire integration."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SmartfireDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Smartfire switch from a config entry."""
    coordinator: SmartfireDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([SmartfireSwitch(coordinator)])


class SmartfireSwitch(CoordinatorEntity[SmartfireDataUpdateCoordinator], SwitchEntity):
    """Representation of a Smartfire fireplace power switch."""

    _attr_has_entity_name = True
    _attr_name = "Fireplace"
    _attr_unique_id = "smartfire_power"

    def __init__(self, coordinator: SmartfireDataUpdateCoordinator) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._attr_device_info = coordinator.device_info
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_power"

    @property
    def is_on(self) -> bool:
        """Return true if the fireplace is on."""
        return self.coordinator.data.get("power", False)

    async def async_turn_on(self, **kwargs: object) -> None:
        """Turn the fireplace on."""
        await self.coordinator.async_set_power(True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: object) -> None:
        """Turn the fireplace off."""
        await self.coordinator.async_set_power(False)
        await self.coordinator.async_request_refresh()
