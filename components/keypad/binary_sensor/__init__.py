import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import CONF_ID
from .. import Keypad, keypad_ns, CONF_KEYPAD_ID

CONF_KEY = 'key'
CONF_ROW = 'row'
CONF_COL = 'col'

DEPENDENCIES = ['keypad']

KeypadBinarySensor = keypad_ns.class_('KeypadBinarySensor', binary_sensor.BinarySensor)

def check_button(obj):
    if CONF_ROW in obj or CONF_COL in obj:
        if CONF_KEY in obj:
            raise cv.Invalid("You can't provide both a key and a position")
        elif CONF_ROW not in obj:
            raise cv.Invalid("Missing row")
        elif CONF_COL not in obj:
            raise cv.Invalid("Missing col")
    elif CONF_KEY not in obj:
        raise cv.Invalid("Missing key or position")
    elif len(obj[CONF_KEY]) != 1:
        raise cv.Invalid("Key must be one character")
    return obj

CONFIG_SCHEMA = cv.All(binary_sensor.BINARY_SENSOR_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(KeypadBinarySensor),
    cv.GenerateID(CONF_KEYPAD_ID): cv.use_id(Keypad),
    cv.Optional(CONF_ROW): cv.int_,
    cv.Optional(CONF_COL): cv.int_,
    cv.Optional(CONF_KEY): cv.string,
}), check_button)


async def to_code(config):
    if CONF_KEY in config:
      var = cg.new_Pvariable(config[CONF_ID], config[CONF_KEY][0])
    else:
      var = cg.new_Pvariable(config[CONF_ID], config[CONF_ROW], config[CONF_COL])
    await binary_sensor.register_binary_sensor(var, config)
    keypad = await cg.get_variable(config[CONF_KEYPAD_ID])
    cg.add(keypad.register_listener(var))
