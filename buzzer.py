from gpiozero import Buzzer
from time import sleep

pin = Buzzer(16)


def buzz():
    pin.on()
    sleep(.5)
    pin.off()
    sleep(.5)
