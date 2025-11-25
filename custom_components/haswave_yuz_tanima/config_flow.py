"""Config flow for HasWave Yüz Tanıma integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, DEFAULT_TOLERANCE, DEFAULT_DETECTION_INTERVAL, DEFAULT_MIN_FACE_SIZE

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("camera_url"): str,
        vol.Optional("faces_directory", default="/config/www/yuzler"): str,
        vol.Optional("tolerance", default=DEFAULT_TOLERANCE): float,
        vol.Optional("detection_interval", default=DEFAULT_DETECTION_INTERVAL): int,
        vol.Optional("min_face_size", default=DEFAULT_MIN_FACE_SIZE): int,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HasWave Yüz Tanıma."""
    
    VERSION = 1
    
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )
        
        return self.async_create_entry(title="HasWave Yüz Tanıma", data=user_input)

