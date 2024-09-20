import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.components import uart
from esphome.const import CONF_ID

DEPENDENCIES = ['uart']

ifan_ns = cg.esphome_ns.namespace('ifan')
IFan = ifan_ns.class_('IFan', cg.Component)

CONF_BUZZER_SWITCH = 'buzzer_switch'
CONF_REMOTE_SWITCH = 'remote_switch'

CONFIG_SCHEMA = cv.All(
    switch.switch_schema(IFan).extend({
        cv.Optional(CONF_BUZZER_SWITCH): switch.SWITCH_SCHEMA,
        cv.Optional(CONF_REMOTE_SWITCH): switch.SWITCH_SCHEMA,
    }).extend(cv.COMPONENT_SCHEMA)
)


async def to_code(config):
    fan_component = await cg.get_variable(config[CONF_ID])
    
    if CONF_BUZZER_SWITCH in config:
        buzzer_switch = await switch.new_switch(config[CONF_BUZZER_SWITCH])
        cg.add(fan_component.set_buzzer_enabled(buzzer_switch))

    if CONF_REMOTE_SWITCH in config:
        remote_switch = await switch.new_switch(config[CONF_REMOTE_SWITCH])
        cg.add(fan_component.set_remote_enabled(remote_switch))
