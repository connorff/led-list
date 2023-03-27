# led-list

Teach Python lists with a [BlinkStick Flex](https://www.blinkstick.com/products/blinkstick-flex)! Each LED represents a list index which can change color and turn off.

# Examples

## Turn on all LEDs
```python
from led_list import LEDList

# initialize list with all lights (32) colored white
l = LEDList(["white"] * 32)
```

## Change specific index
```python
from led_list import LEDList

# initialize list with all lights (32) colored white
l = LEDList(["white"] * 32)

# change first light to red
l[0] = "red"

# change second light to custom RGB value
l[1] = (255, 50, 50)
```

## Turn off lights
```python
from led_list import LEDList

# initialize list with all lights (32) colored white
l = LEDList(["white"] * 32)

# turn off every light sequentially
for x in range(len(l)):
    l[x] = "black"
```
