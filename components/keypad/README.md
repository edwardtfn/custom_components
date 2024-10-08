# keypad component

This component matrix keypads.  Define a `keypad` component then add `binary_sensor`s or a `text_sensor` to handle the keys.

The `keys` parameter is optional for the `keypad`, but then you won't be able to check for it in the `binary_sensor`
and the `text_sensor` won't work.
The optional `has_diodes` parameter is for if the buttons have diodes and the row pins are output only. In that case, set it to true.

For the `binary_sensor`, you need to provide either the `row` and `col` or the `key` parameter.

For the `text_sensor`, you need at least one of the `end_keys` or `max_length` parameters.  The rest are optional.

Example:
```yaml
keypad:
  id: mykeypad
  rows:
    - pin: 21
    - pin: 19
    - pin: 18
    - pin: 5
  columns:
    - pin: 17
    - pin: 16
    - pin: 4
    - pin: 15
  keys: "123A456B789C*0#D"
  has_diodes: false

binary_sensor:
  - platform: keypad
    keypad_id: mykeypad
    id: key4
    row: 1
    col: 0
  - platform: keypad
    id: keyA
    key: A

text_sensor:
  - platform: keypad
    id: reader
    keypad_id: mykeypad
    min_length: 4
    max_length: 4
    end_keys: "#"
    end_key_required: true   # default is false
    back_keys: "*"
    clear_keys: "C"
    timeout: 5s
    allowed_keys: "0123456789"
    on_progress:
      - logger.log: 
          format: "input progress: '%s'"
          args: [ 'x.c_str()' ]
    on_value:
      - logger.log: 
          format: "input result: '%s'"
          args: [ 'x.c_str()' ]
```

