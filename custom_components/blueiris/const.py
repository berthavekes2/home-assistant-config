"""
Support for Blue Iris.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/switch.blueiris/
"""
from datetime import timedelta
import voluptuous as vol

from homeassistant.const import (
    CONF_HOST, CONF_PORT, CONF_PASSWORD,
    CONF_USERNAME, CONF_SSL,
    CONF_ID, CONF_NAME)

from homeassistant.components.binary_sensor import DOMAIN as DOMAIN_BINARY_SENSOR
from homeassistant.components.camera import DOMAIN as DOMAIN_CAMERA
from homeassistant.components.switch import DOMAIN as DOMAIN_SWITCH

from homeassistant.components.mqtt import (
    CONF_PAYLOAD_AVAILABLE, DEFAULT_PAYLOAD_AVAILABLE,
    CONF_QOS, CONF_PAYLOAD_NOT_AVAILABLE, DEFAULT_PAYLOAD_NOT_AVAILABLE,
    DEFAULT_QOS)

VERSION = '2.0.0'

DOMAIN = 'blueiris'
DATA_BLUEIRIS = f'data_{DOMAIN}'
DATA_BLUEIRIS_API = f'{DATA_BLUEIRIS}_API'
DATA_BLUEIRIS_HA = f'{DATA_BLUEIRIS}_HA'
DATA_BLUEIRIS_HA_ENTITIES = f'{DATA_BLUEIRIS}_HA_Entities'
DEFAULT_NAME = "BlueIris"
DEFAULT_PORT = 80

DOMAIN_KEY_FILE = f"{DOMAIN}.key"

ATTR_ADMIN_PROFILE = 'Profile'
ATTR_SYSTEM_CAMERA_ALL_NAME = 'All'
ATTR_SYSTEM_CAMERA_ALL_ID = 'Index'
ATTR_SYSTEM_CAMERA_CYCLE_NAME = 'Cycle'
ATTR_SYSTEM_CAMERA_CYCLE_ID = '@Index'

AUDIO_EVENT_LENGTH = 2
RECONNECT_DELAY = 15

BLUEIRIS_AUTH_ERROR = "Authorization required"

SYSTEM_CAMERA_CONFIG = {
    ATTR_SYSTEM_CAMERA_ALL_NAME: ATTR_SYSTEM_CAMERA_ALL_ID,
    ATTR_SYSTEM_CAMERA_CYCLE_NAME: ATTR_SYSTEM_CAMERA_CYCLE_ID
}

SYSTEM_CAMERA_ID = [
    ATTR_SYSTEM_CAMERA_ALL_ID,
    ATTR_SYSTEM_CAMERA_CYCLE_ID
]

MQTT_AVAILABILITY_CONFIG = {
    CONF_PAYLOAD_AVAILABLE: DEFAULT_PAYLOAD_AVAILABLE,
    CONF_PAYLOAD_NOT_AVAILABLE: DEFAULT_PAYLOAD_NOT_AVAILABLE,
    CONF_QOS: DEFAULT_QOS
}

AUTHENTICATION_BASIC = 'basic'

NOTIFICATION_ID = f'{DOMAIN}_notification'
NOTIFICATION_TITLE = f'{DEFAULT_NAME} Setup'

DEFAULT_ICON = 'mdi:alarm-light'

CAMERA_ID_PLACEHOLDER = '[camera_id]'

ATTR_FRIENDLY_NAME = 'friendly_name'

PROTOCOLS = {
    True: 'https',
    False: 'http'
}

SCAN_INTERVAL = timedelta(seconds=30)

DEFAULT_FORCE_UPDATE = False

SENSOR_CONNECTIVITY_NAME = 'Connectivity'
SENSOR_MOTION_NAME = 'Motion'
SENSOR_AUDIO_NAME = 'Audio'
SENSOR_MAIN_NAME = 'Main'

SENSOR_DEVICE_CLASS = {
    SENSOR_AUDIO_NAME: 'sound'
}

MQTT_MESSAGE_TRIGGER = 'trigger'
MQTT_MESSAGE_TYPE = 'type'
MQTT_MESSAGE_VALUE_UNKNOWN = 'unknown'

MQTT_ALL_TOPIC = "BlueIris/+/Status"

CONFIG_OPTIONS = 'options'
CONFIG_CONDITIONS = 'conditions'
CONFIG_ITEMS = 'items'

ATTR_BLUE_IRIS_CAMERA = {
    "optionDisplay": CONF_NAME,
    "optionValue": CONF_ID,
    "FPS": "FPS",
    "audio": "Audio support",
    "width": "Width",
    "height": "Height",
    "isOnline": "Is Online",
    "isRecording": "Is Recording",
    "isYellow": "Issue",
    "nAlerts": "Alerts #",
    "nTriggers": "Triggers #",
    "nClips": "Clips #",
    "nNoSignal": "No Signal #",
    "error": "Error"
}
ATTR_BLUE_IRIS_STATUS = [
    "system name",
    "version",
    "license",
    "support",
    "user",
    "latitude",
    "longitude"
]

BI_DISCOVERY = f"{DOMAIN}_discovery"
BI_DISCOVERY_BINARY_SENSOR = f"{BI_DISCOVERY}_{DOMAIN_BINARY_SENSOR}"
BI_DISCOVERY_CAMERA = f"{BI_DISCOVERY}_{DOMAIN_CAMERA}"
BI_DISCOVERY_SWITCH = f"{BI_DISCOVERY}_{DOMAIN_SWITCH}"

BI_UPDATE_SIGNAL_CAMERA = f"{DOMAIN}_{DOMAIN_CAMERA}_UPDATE_SIGNAL"
BI_UPDATE_SIGNAL_BINARY_SENSOR = f"{DOMAIN}_{DOMAIN_BINARY_SENSOR}_UPDATE_SIGNAL"
BI_UPDATE_SIGNAL_SWITCH = f"{DOMAIN}_{DOMAIN_SWITCH}_UPDATE_SIGNAL"

CONFIG_FIELDS = {
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_PORT): int,
    vol.Optional(CONF_SSL, default=False): bool,
    vol.Optional(CONF_USERNAME): str,
    vol.Optional(CONF_PASSWORD): str,
}

SUPPORTED_DOMAINS = [DOMAIN_SWITCH, DOMAIN_BINARY_SENSOR, DOMAIN_CAMERA]
SIGNALS = {
    DOMAIN_BINARY_SENSOR: BI_UPDATE_SIGNAL_BINARY_SENSOR,
    DOMAIN_CAMERA: BI_UPDATE_SIGNAL_CAMERA,
    DOMAIN_SWITCH: BI_UPDATE_SIGNAL_SWITCH
}

ENTITY_ID = "id"
ENTITY_NAME = "name"
ENTITY_STATE = "state"
ENTITY_ATTRIBUTES = "attributes"
ENTITY_ICON = "icon"
ENTITY_UNIQUE_ID = "unique-id"
ENTITY_EVENT = "event-type"
ENTITY_TOPIC = "topic"
ENTITY_DEVICE_CLASS = "device-class"
ENTITY_DEVICE_NAME = "device-name"
ENTITY_CAMERA_DETAILS = "camera-details"
ENTITY_BINARY_SENSOR_TYPE = "binary-sensor-type"

CONF_EXCLUDE_SYSTEM_CAMERA = "exclude-system-camera"
CONF_CLEAR_CREDENTIALS = "clear-credentials"

DOMAIN_LOAD = "load"
DOMAIN_UNLOAD = "unload"
