from typing import List, Tuple
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

    # cached value of LED values
    __cache = []

    def __init__(self, initlist):
        super().__init__(initlist)
        
        # turn off LEDs when deconstructed
        atexit.register(self.cleanup)

        # light up
        self.__light()

    # find updated LED values between incoming list and cached list
    @staticmethod
    def __light_diff(new: List, cached: List) -> List[Tuple]:
        new = LEDList.__leds_to_tuple(new)
        updates = []

        # find overlap of new and cached lights
        overlap = min(len(new), len(cached))
        for index, values in enumerate(zip(new[0:overlap], cached[0:overlap])):
            if values[0] != values[1]:
                updates.append((index, values[0]))

        if len(new) > len(cached):
            # find lights to turn on
            new = new[overlap:]
            updates.extend(enumerate(new, overlap))
        else:
            # find lights to turn off (reverse order)
            off = [(0, 0, 0)] * (len(cached) - overlap)
            updates.extend(reversed(list(enumerate(off, overlap))))

        return updates

    # convert string color values to tuples
    @staticmethod
    def __leds_to_tuple(leds: List) -> List[Tuple]:
        rgbs = []

        for led in leds:
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

            rgbs.append(led)

        return rgbs

    def __light(self):
        updates = self.__light_diff(self.data, self.__cache)

        for index, led in updates:
            self.bstick.set_color(channel=0, index=index, red=led[0], green=led[1], blue=led[2])

        self.__cache = self.__leds_to_tuple(self.data)

    def set(self, new: List) -> None:
        self.data = new
        self.__light()

        return

    def remove(self, item) -> None:
        super().remove(item)
        self.__light()

        return

    def append(self, item) -> None:
        super().append(item)
        self.__light()

        return
    
    def extend(self, other):
        super().extend(other)
        self.__light()

        return

    def cleanup(self):
        for x in range(len(self.data)):
            self.bstick.set_color(channel=0, index=x, name="off")

    def __setitem__(self, index, value):
        self.data[index] = value
        self.__light()

        return
