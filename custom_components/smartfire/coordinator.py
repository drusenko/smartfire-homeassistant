"""Data update coordinator for Smartfire integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SmartfireApiClient, SmartfireApiClientCommunicationError

from .const import DOMAIN, LOGGER


class SmartfireDataUpdateCoordinator(DataUpdateCoordinator[dict]):
    """Class to manage fetching Smartfire data."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: SmartfireApiClient,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self._client = client
        self.config_entry = entry

        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Smartfire Fireplace",
            manufacturer="Sit Group",
            model="Proflame 2",
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from the API."""
        try:
            power = await self._client.async_get_power()
            return {"power": power}
        except SmartfireApiClientCommunicationError as err:
            raise UpdateFailed(str(err)) from err

    async def async_set_power(self, power: bool) -> None:
        """Set the power state."""
        await self._client.async_set_power(power)
