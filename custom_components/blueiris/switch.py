"""
Support for Blue Iris.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.blueiris/
"""
import sys
import logging
from typing import Optional

from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.components.switch import SwitchDevice

from .const import *

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = [DOMAIN]

CURRENT_DOMAIN = DOMAIN_SWITCH


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Set up the EdgeOS Binary Sensor."""
    _LOGGER.debug(f"Starting async_setup_entry {CURRENT_DOMAIN}")

    try:
        entry_data = config_entry.data
        host = entry_data.get(CONF_HOST)
        entities = []

        ha = _get_ha(hass, host)
        entity_manager = ha.entity_manager

        if entity_manager is not None:
            entities_data = entity_manager.get_entities(CURRENT_DOMAIN)
            for entity_name in entities_data:
                entity = entities_data[entity_name]

                entity = BlueIrisProfileSwitch(hass, host, entity)

                _LOGGER.debug(f"Setup {CURRENT_DOMAIN}: {entity.name} | {entity.unique_id}")

                entities.append(entity)

                entity_manager.set_entry_loaded_state(CURRENT_DOMAIN, True)

        async_add_devices(entities, True)
    except Exception as ex:
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno

        _LOGGER.error(f"Failed to load {CURRENT_DOMAIN}, error: {ex}, line: {line_number}")


async def async_unload_entry(hass, config_entry):
    _LOGGER.info(f"async_unload_entry {CURRENT_DOMAIN}: {config_entry}")

    entry_data = config_entry.data
    host = entry_data.get(CONF_HOST)

    ha = _get_ha(hass, host)
    entity_manager = ha.entity_manager

    if entity_manager is not None:
        entity_manager.set_entry_loaded_state(CURRENT_DOMAIN, False)

    return True


class BlueIrisProfileSwitch(SwitchDevice):
    """An abstract class for an Blue Iris arm switch."""
    def __init__(self, hass, integration_name, entity):
        """Initialize the settings switch."""
        super().__init__()

        self._hass = hass
        self._integration_name = integration_name
        self._entity = entity
        self._remove_dispatcher = None

        self._ha = _get_ha(self._hass, self._integration_name)
        self._entity_manager = self._ha.entity_manager
        self._device_manager = self._ha.device_manager
        self._api = self._ha.api

    @property
    def profile_id(self):
        return self._entity.get(ENTITY_ID)

    @property
    def unique_id(self) -> Optional[str]:
        """Return the name of the node."""
        return self._entity.get(ENTITY_UNIQUE_ID)

    @property
    def device_info(self):
        device_name = self._entity.get(ENTITY_DEVICE_NAME)

        return self._device_manager.get(device_name)

    @property
    def name(self):
        """Return the name of the node."""
        return self._entity.get(ENTITY_NAME)

    async def async_added_to_hass(self):
        """Register callbacks."""
        self._remove_dispatcher = async_dispatcher_connect(self.hass, SIGNALS[CURRENT_DOMAIN], self.update_data)

    async def async_will_remove_from_hass(self) -> None:
        if self._remove_dispatcher is not None:
            self._remove_dispatcher()

    @property
    def is_on(self):
        """Return the boolean response if the node is on."""
        return self._entity.get(ENTITY_STATE)

    async def async_turn_on(self, **kwargs):
        """Turn device on."""
        await self.set_profile(self.profile_id)

    async def async_turn_off(self, **kwargs):
        """Turn device off."""
        to_profile_id = 1
        if self.profile_id == 1:
            to_profile_id = 0

        await self.set_profile(to_profile_id)

    async def set_profile(self, profile_id):
        await self._api.set_profile(profile_id)

        await self._ha.async_update(None)

    @property
    def icon(self):
        """Return the icon for the switch."""
        return self._entity.get(ENTITY_ICON)

    def turn_on(self, **kwargs) -> None:
        pass

    def turn_off(self, **kwargs) -> None:
        pass

    async def async_setup(self):
        pass

    @callback
    def update_data(self):
        self.hass.async_add_job(self.async_update_data)

    async def async_update_data(self):
        if self._entity_manager is None:
            _LOGGER.debug(f"Cannot update {CURRENT_DOMAIN} - Entity Manager is None | {self.name}")
        else:
            previous_state = self.is_on
            self._entity = self._entity_manager.get_entity(CURRENT_DOMAIN, self.name)

            current_state = self.is_on
            state_changed = previous_state != current_state

            if self._entity is None:
                _LOGGER.debug(f"Cannot update {CURRENT_DOMAIN} - Entity was not found | {self.name}")

                self._entity = {}
                await self.async_remove()
            else:
                if state_changed:
                    _LOGGER.debug(f"Update {CURRENT_DOMAIN} -> {self.name}, from: {previous_state} to {current_state}")

                    self.async_schedule_update_ha_state(True)


def _get_ha(hass, host):
    ha_data = hass.data.get(DATA_BLUEIRIS, {})
    ha = ha_data.get(host)

    return ha
