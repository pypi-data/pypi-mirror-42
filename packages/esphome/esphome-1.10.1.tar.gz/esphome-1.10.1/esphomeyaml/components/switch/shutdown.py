import voluptuous as vol

import esphomeyaml.config_validation as cv
from esphomeyaml.components import switch
from esphomeyaml.const import CONF_INVERTED, CONF_MAKE_ID, CONF_NAME
from esphomeyaml.cpp_generator import variable
from esphomeyaml.cpp_types import Application, App

MakeShutdownSwitch = Application.struct('MakeShutdownSwitch')
ShutdownSwitch = switch.switch_ns.class_('ShutdownSwitch', switch.Switch)

PLATFORM_SCHEMA = cv.nameable(switch.SWITCH_PLATFORM_SCHEMA.extend({
    cv.GenerateID(): cv.declare_variable_id(ShutdownSwitch),
    cv.GenerateID(CONF_MAKE_ID): cv.declare_variable_id(MakeShutdownSwitch),
    vol.Optional(CONF_INVERTED): cv.invalid("Shutdown switches do not support inverted mode!"),
}))


def to_code(config):
    rhs = App.make_shutdown_switch(config[CONF_NAME])
    shutdown = variable(config[CONF_MAKE_ID], rhs)
    switch.setup_switch(shutdown.Pshutdown, shutdown.Pmqtt, config)


BUILD_FLAGS = '-DUSE_SHUTDOWN_SWITCH'


def to_hass_config(data, config):
    return switch.core_to_hass_config(data, config)
