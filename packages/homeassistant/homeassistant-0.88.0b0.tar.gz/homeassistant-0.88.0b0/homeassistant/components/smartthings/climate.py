"""Support for climate devices through the SmartThings cloud API."""
import asyncio

from homeassistant.components.climate import (
    ATTR_OPERATION_MODE, ATTR_TARGET_TEMP_HIGH, ATTR_TARGET_TEMP_LOW,
    ATTR_TEMPERATURE, STATE_AUTO, STATE_COOL, STATE_ECO, STATE_HEAT, STATE_OFF,
    SUPPORT_FAN_MODE, SUPPORT_OPERATION_MODE, SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_TEMPERATURE_HIGH, SUPPORT_TARGET_TEMPERATURE_LOW,
    ClimateDevice)
from homeassistant.const import TEMP_CELSIUS, TEMP_FAHRENHEIT

from . import SmartThingsEntity
from .const import DATA_BROKERS, DOMAIN

DEPENDENCIES = ['smartthings']

ATTR_OPERATION_STATE = 'operation_state'
MODE_TO_STATE = {
    'auto': STATE_AUTO,
    'cool': STATE_COOL,
    'eco': STATE_ECO,
    'rush hour': STATE_ECO,
    'emergency heat': STATE_HEAT,
    'heat': STATE_HEAT,
    'off': STATE_OFF
}
STATE_TO_MODE = {
    STATE_AUTO: 'auto',
    STATE_COOL: 'cool',
    STATE_ECO: 'eco',
    STATE_HEAT: 'heat',
    STATE_OFF: 'off'
}
UNIT_MAP = {
    'C': TEMP_CELSIUS,
    'F': TEMP_FAHRENHEIT
}


async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):
    """Platform uses config entry setup."""
    pass


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add climate entities for a config entry."""
    broker = hass.data[DOMAIN][DATA_BROKERS][config_entry.entry_id]
    async_add_entities(
        [SmartThingsThermostat(device) for device in broker.devices.values()
         if is_climate(device)])


def is_climate(device):
    """Determine if the device should be represented as a climate entity."""
    from pysmartthings import Capability

    # Can have this legacy/deprecated capability
    if Capability.thermostat in device.capabilities:
        return True
    # Or must have all of these
    climate_capabilities = [
        Capability.temperature_measurement,
        Capability.thermostat_cooling_setpoint,
        Capability.thermostat_heating_setpoint,
        Capability.thermostat_mode]
    if all(capability in device.capabilities
           for capability in climate_capabilities):
        return True
    # Optional capabilities:
    # relative_humidity_measurement -> state attribs
    # thermostat_operating_state -> state attribs
    # thermostat_fan_mode -> SUPPORT_FAN_MODE
    return False


class SmartThingsThermostat(SmartThingsEntity, ClimateDevice):
    """Define a SmartThings climate entities."""

    def __init__(self, device):
        """Init the class."""
        super().__init__(device)
        self._supported_features = self._determine_features()

    def _determine_features(self):
        from pysmartthings import Capability

        flags = SUPPORT_OPERATION_MODE \
            | SUPPORT_TARGET_TEMPERATURE \
            | SUPPORT_TARGET_TEMPERATURE_LOW \
            | SUPPORT_TARGET_TEMPERATURE_HIGH
        if self._device.get_capability(
                Capability.thermostat_fan_mode, Capability.thermostat):
            flags |= SUPPORT_FAN_MODE
        return flags

    async def async_set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        await self._device.set_thermostat_fan_mode(fan_mode, set_status=True)

        # State is set optimistically in the command above, therefore update
        # the entity state ahead of receiving the confirming push updates
        self.async_schedule_update_ha_state(True)

    async def async_set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        mode = STATE_TO_MODE[operation_mode]
        await self._device.set_thermostat_mode(mode, set_status=True)

        # State is set optimistically in the command above, therefore update
        # the entity state ahead of receiving the confirming push updates
        self.async_schedule_update_ha_state(True)

    async def async_set_temperature(self, **kwargs):
        """Set new operation mode and target temperatures."""
        # Operation state
        operation_state = kwargs.get(ATTR_OPERATION_MODE)
        if operation_state:
            mode = STATE_TO_MODE[operation_state]
            await self._device.set_thermostat_mode(mode, set_status=True)

        # Heat/cool setpoint
        heating_setpoint = None
        cooling_setpoint = None
        if self.current_operation == STATE_HEAT:
            heating_setpoint = kwargs.get(ATTR_TEMPERATURE)
        elif self.current_operation == STATE_COOL:
            cooling_setpoint = kwargs.get(ATTR_TEMPERATURE)
        else:
            heating_setpoint = kwargs.get(ATTR_TARGET_TEMP_LOW)
            cooling_setpoint = kwargs.get(ATTR_TARGET_TEMP_HIGH)
        tasks = []
        if heating_setpoint is not None:
            tasks.append(self._device.set_heating_setpoint(
                round(heating_setpoint, 3), set_status=True))
        if cooling_setpoint is not None:
            tasks.append(self._device.set_cooling_setpoint(
                round(cooling_setpoint, 3), set_status=True))
        await asyncio.gather(*tasks)

        # State is set optimistically in the commands above, therefore update
        # the entity state ahead of receiving the confirming push updates
        self.async_schedule_update_ha_state(True)

    @property
    def current_fan_mode(self):
        """Return the fan setting."""
        return self._device.status.thermostat_fan_mode

    @property
    def current_humidity(self):
        """Return the current humidity."""
        return self._device.status.humidity

    @property
    def current_operation(self):
        """Return current operation ie. heat, cool, idle."""
        return MODE_TO_STATE[self._device.status.thermostat_mode]

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._device.status.temperature

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return {
            ATTR_OPERATION_STATE:
                self._device.status.thermostat_operating_state
        }

    @property
    def fan_list(self):
        """Return the list of available fan modes."""
        return self._device.status.supported_thermostat_fan_modes

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return {MODE_TO_STATE[mode] for mode in
                self._device.status.supported_thermostat_modes}

    @property
    def supported_features(self):
        """Return the supported features."""
        return self._supported_features

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        if self.current_operation == STATE_COOL:
            return self._device.status.cooling_setpoint
        if self.current_operation == STATE_HEAT:
            return self._device.status.heating_setpoint
        return None

    @property
    def target_temperature_high(self):
        """Return the highbound target temperature we try to reach."""
        if self.current_operation == STATE_AUTO:
            return self._device.status.cooling_setpoint
        return None

    @property
    def target_temperature_low(self):
        """Return the lowbound target temperature we try to reach."""
        if self.current_operation == STATE_AUTO:
            return self._device.status.heating_setpoint
        return None

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return UNIT_MAP.get(
            self._device.status.attributes['temperature'].unit)
