"""Config flow to configure Z-Wave."""
from collections import OrderedDict
import logging
import os
import stat

import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, CONF_CODE, CONF_SERIAL_PORT

_LOGGER = logging.getLogger(__name__)

@config_entries.HANDLERS.register(DOMAIN)
class DuofernFlowHandler(config_entries.ConfigFlow):
    """Handle a Z-Wave config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize the Z-Wave config flow."""
        self.serial_port = CONF_SERIAL_PORT

    async def async_step_user(self, user_input=None):
        """Handle a flow start."""
        if self._async_current_entries():
            return self.async_abort(reason='one_instance_only')

        errors = {}

        fields = OrderedDict()
        fields[vol.Required(CONF_SERIAL_PORT,
                            default="/dev/ttyUSB0")] = str
        fields[vol.Required(CONF_CODE)] = str

        if user_input is not None:
            try:
                int(user_input[CONF_CODE], 16)
                conv_error = False
            except ValueError:
                conv_error = True
            if not stat.S_ISCHR(os.stat(user_input[CONF_SERIAL_PORT]).st_mode) or \
                    len(user_input[CONF_CODE]) != 4 or conv_error:
                errors['base'] = 'option_error'
                return self.async_show_form(
                    step_id='user',
                    data_schema=vol.Schema(fields),
                    errors=errors
                )

            return self.async_create_entry(
                title='duofern',
                data={
                    CONF_SERIAL_PORT: user_input[CONF_SERIAL_PORT],
                    CONF_CODE: user_input[CONF_CODE],
                },
            )

        return self.async_show_form(
          step_id='user', data_schema=vol.Schema(fields)
        )

#    async def async_step_import(self, info):
#        """Import existing configuration from Z-Wave."""
#        if self._async_current_entries():
#            return self.async_abort(reason='already_setup')

#        return self.async_create_entry(
#            title="Z-Wave (import from configuration.yaml)",
#            data={
#                CONF_SERIAL_PORT: info.get(CONF_SERIAL_PORT),
#                CONF_CODE: info.get(CONF_CODE),
#            },
#        )
