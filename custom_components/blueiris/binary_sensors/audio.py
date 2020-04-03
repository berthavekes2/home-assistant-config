import asyncio
import logging
from datetime import datetime

from homeassistant.components.binary_sensor import STATE_OFF

from custom_components.blueiris.const import *
from .base import BlueIrisBinarySensor

_LOGGER = logging.getLogger(__name__)


class BlueIrisAudioBinarySensor(BlueIrisBinarySensor):
    """Representation a binary sensor that is updated by MQTT."""

    def __init__(self, hass, integration_name, entity):
        """Initialize the MQTT binary sensor."""
        super().__init__(hass, integration_name, entity)

        self._last_alert = None

    def perform_update(self):
        is_trigger_off = self.state == STATE_OFF
        current_timestamp = datetime.now().timestamp()

        _LOGGER.info(f"Performing update, state: {is_trigger_off}, last: {self._last_alert}, ts: {current_timestamp}")

        if is_trigger_off:
            self._last_alert = None
            super().perform_update()

        else:
            if self._last_alert is None or current_timestamp - self._last_alert > AUDIO_EVENT_LENGTH:
                self._last_alert = current_timestamp
                super().perform_update()

                self.hass.async_create_task(self.turn_off_automatically())

    async def turn_off_automatically(self):
        await asyncio.sleep(AUDIO_EVENT_LENGTH)

        _LOGGER.info(f"Turn off audio alert for {self.name}")

        self._entity_manager.set_mqtt_state(self.topic, self.event_type, False)

        self.hass.async_create_task(self._ha.async_update(None))
