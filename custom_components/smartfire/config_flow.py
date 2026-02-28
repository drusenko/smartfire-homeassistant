"""Config flow for Smartfire integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SmartfireApiClient
from .const import (
    CONF_BASE_URL,
    CONF_INSTALL_TYPE,
    DEFAULT_LOCAL_URL,
    DEFAULT_PORT,
    DOMAIN,
    INSTALL_TYPE_LOCAL,
    INSTALL_TYPE_REMOTE,
    LOGGER,
)


def _build_remote_url(host: str, port: int) -> str:
    """Build base URL from host and port."""
    return f"http://{host}:{port}"


async def _test_connection(hass: HomeAssistant, base_url: str) -> bool:
    """Test connection to the Smartfire server."""
    session = async_get_clientsession(hass)
    client = SmartfireApiClient(base_url, session)
    return await client.async_test_connection()


class SmartfireConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Smartfire."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> FlowResult:
        """Handle the initial step - choose install type."""
        if user_input is not None:
            install_type = user_input[CONF_INSTALL_TYPE]
            if install_type == INSTALL_TYPE_LOCAL:
                return await self.async_step_local()
            return await self.async_step_remote()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_INSTALL_TYPE): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                selector.SelectOptionDict(
                                    value=INSTALL_TYPE_LOCAL,
                                    label="Local (YardStick connected to this Home Assistant server)",
                                ),
                                selector.SelectOptionDict(
                                    value=INSTALL_TYPE_REMOTE,
                                    label="Remote (Smartfire REST server on another device)",
                                ),
                            ],
                            mode=selector.SelectSelectorMode.DROPDOWN,
                        )
                    ),
                }
            ),
        )

    async def async_step_local(
        self,
        user_input: dict | None = None,
    ) -> FlowResult:
        """Handle local installation configuration."""
        errors: dict[str, str] = {}

        base_url = DEFAULT_LOCAL_URL

        if user_input is not None:
            # Test connection to local server
            if await _test_connection(self.hass, base_url):
                return self.async_create_entry(
                    title="Smartfire (Local)",
                    data={
                        CONF_INSTALL_TYPE: INSTALL_TYPE_LOCAL,
                        CONF_BASE_URL: base_url,
                    },
                )
            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="local",
            data_schema=vol.Schema(
                {
                    vol.Required("addon_ready", default=False): selector.BooleanSelector(
                        selector.BooleanSelectorConfig(
                            label="I have installed the Smartfire Server add-on and it is running"
                        )
                    ),
                }
            ),
            description="For local installations, you must install and run the Smartfire Server add-on. Go to Settings → Add-ons → Add-on store → Add repository, then add this repository URL. Install the 'Smartfire Server' add-on, start it, and ensure the YardStick One is connected via USB.",
            errors=errors,
        )

    async def async_step_remote(
        self,
        user_input: dict | None = None,
    ) -> FlowResult:
        """Handle remote installation configuration."""
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            base_url = _build_remote_url(host, port)

            try:
                if await _test_connection(self.hass, base_url):
                    return self.async_create_entry(
                        title=f"Smartfire ({host}:{port})",
                        data={
                            CONF_INSTALL_TYPE: INSTALL_TYPE_REMOTE,
                            CONF_BASE_URL: base_url,
                            CONF_HOST: host,
                            CONF_PORT: port,
                        },
                    )
            except Exception as exc:  # pylint: disable=broad-except
                LOGGER.exception("Error testing connection: %s", exc)

            errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="remote",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST, default=(user_input or {}).get(CONF_HOST, "")): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                            autocomplete="url",
                        )
                    ),
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {}).get(CONF_PORT, DEFAULT_PORT),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=1,
                            max=65535,
                            step=1,
                            mode=selector.NumberSelectorMode.BOX,
                        )
                    ),
                }
            ),
            errors=errors,
        )
