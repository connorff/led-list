from blinkstick import blinkstick
from collections import UserList
import atexit

PRESET_COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "orange": (255, 50, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "purple": (143, 0, 255),
    "pink": (255, 0, 232),
}
PRESET_KEYS = ", ".join(PRESET_COLORS.keys())

class LEDList(UserList):
    # number of LEDs on the device
    NUM_LEDS = 32

    # connected blinkstick device
    bstick = blinkstick.find_first()

    def __init__(self, initlist):
        super().__init__(initlist)
        
        # turn off LEDs when deconstructed
        atexit.register(self.cleanup)

        # light up
        self.__light__()

    def __light__(self):
        for index, led in enumerate(self.data):
            # convert string colors to tuple
            if isinstance(led, str):
                if led in PRESET_COLORS:
                    led = PRESET_COLORS[led]
                else:
                    raise ValueError(f"Unrecognized color {led}. Valid options are {PRESET_KEYS}.")

            # ensure LED color has either three or zero channels
            if len(led) != 3 and len(led) != 0:
                raise ValueError(f"LED color must have three or zero channels. Reading {led}.")

            # empty LED should be off
            if len(led) == 0:
                led = (0, 0, 0)

            self.bstick.set_color(channel=0, index=index, red=led[0], green=led[1], blue=led[2])

        for led in range(self.NUM_LEDS - len(self.data)):
            self.bstick.set_color(channel=0, index=len(self.data) + led, name="off")

    def remove(self, item) -> None:
        super().remove(item)
        self.__light__()

        return

    def append(self, item) -> None:
        super().append(item)
        self.__light__()

        return
    
    def extend(self, other):
        super().extend(other)
        self.__light__()

        return

    def cleanup(self):
        for x in range(len(self.data)):
            self.bstick.set_color(channel=0, index=x, name="off")

    def __setitem__(self, index, value):
        self.data[index] = value
        self.__light__()

        return
