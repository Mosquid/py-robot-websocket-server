from gpiozero import DigitalOutputDevice
from time import sleep

clock = DigitalOutputDevice(23)
latch = DigitalOutputDevice(24)
data = DigitalOutputDevice(20)
blanks = [0, 0, 0, 0, 0]


def linear():
    seq = [
          [1, 0, 0],
          [1, 1, 0],
          [1, 1, 1],
          [1, 1, 1],
          [1, 1, 1],
          [1, 1, 1],
          [0, 0, 0],
    ]

    for l in seq:
        shift_update(l + blanks)
        sleep(.25)


def police_blink():
    seq = [
        [1, 1, 1],
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
        [1, 0, 1],
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 0],
    ]

    for l in seq:
        shift_update(l + blanks)
        sleep(.1)


def shift_update(input):
    global registers
    # put latch down to start data sending
    clock.off()
    latch.off()
    clock.on()

    # load data in reverse order
    for i in range(7, -1, -1):
        clock.off()

        if input[i] == 1:
            data.on()
        else:
            data.off()

        clock.on()

    # put latch up to store data on register
    clock.off()
    latch.on()
    clock.on()
