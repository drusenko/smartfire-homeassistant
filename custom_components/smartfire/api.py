"""API client for the Smartfire REST server."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
from aiohttp import ClientTimeout

from .const import LOGGER


class SmartfireApiClientError(Exception):
    """Exception to indicate a general API error."""


class SmartfireApiClientCommunicationError(SmartfireApiClientError):
    """Exception to indicate a communication error."""


class SmartfireApiClient:
    """Client for the Smartfire REST API."""

    def __init__(self, base_url: str, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._base_url = base_url.rstrip("/")
        self._session = session
        self._timeout = ClientTimeout(total=10)

    def _url(self, path: str) -> str:
        """Build full URL for a path."""
        return f"{self._base_url}{path}"

    async def async_get_power(self) -> bool:
        """Get the current power state."""
        try:
            async with self._session.get(
                self._url("/power"),
                timeout=self._timeout,
            ) as response:
                response.raise_for_status()
                text = await response.text()
                return text.strip().lower() == "true"
        except TimeoutError as exc:
            msg = f"Timeout connecting to Smartfire server: {exc}"
            LOGGER.error(msg)
            raise SmartfireApiClientCommunicationError(msg) from exc
        except (aiohttp.ClientError, socket.gaierror) as exc:
            msg = f"Error communicating with Smartfire server: {exc}"
            LOGGER.error(msg)
            raise SmartfireApiClientCommunicationError(msg) from exc

    async def async_set_power(self, power: bool) -> bool:
        """Set the power state and return the new state."""
        try:
            async with self._session.put(
                self._url("/power"),
                data="True" if power else "False",
                timeout=self._timeout,
            ) as response:
                response.raise_for_status()
                text = await response.text()
                return text.strip().lower() == "true"
        except TimeoutError as exc:
            msg = f"Timeout connecting to Smartfire server: {exc}"
            LOGGER.error(msg)
            raise SmartfireApiClientCommunicationError(msg) from exc
        except (aiohttp.ClientError, socket.gaierror) as exc:
            msg = f"Error communicating with Smartfire server: {exc}"
            LOGGER.error(msg)
            raise SmartfireApiClientCommunicationError(msg) from exc

    async def async_test_connection(self) -> bool:
        """Test the connection to the Smartfire server."""
        try:
            await self.async_get_power()
            return True
        except SmartfireApiClientError:
            return False
