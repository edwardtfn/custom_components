import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import fan, uart

DEPENDENCIES = ['uart']


ifan04_ns = cg.esphome_ns.namespace('ifan04')
IFan04 = ifan04_ns.class_('IFan04', cg.Component, uart.UARTDevice)

CONF_ON_FAN = "on_fan"
CONF_ON_LIGHT = "on_light"
CONF_ON_BUZZER = "on_buzzer"

CONFIG_SCHEMA = (
    fan.fan_schema(IFan04)
    .extend(cv.Optional(CONF_ON_FAN): automation.validate_automation(single=True))
    .extend(cv.Optional(CONF_ON_LIGHT): automation.validate_automation(single=True))
    .extend(cv.Optional(CONF_ON_BUZZER): automation.validate_automation(single=True))
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    var = await fan.new_fan(config)
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    if CONF_ON_FAN in config:
        await automation.build_automation(
            var.get_fan_trigger(), [(int, "speed")], config[CONF_ON_FAN]
        )
    if CONF_ON_LIGHT in config:
        await automation.build_automation(
            var.get_light_trigger(), [], config[CONF_ON_LIGHT]
        )
    if CONF_ON_BUZZER in config:
        await automation.build_automation(
            var.get_buzzer_trigger(), [], config[CONF_ON_BUZZER]
        )

