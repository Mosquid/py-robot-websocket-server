import asyncio
import time
import websockets
from gpiozero import Motor
import json
import threading
from buzzer import buzz

from lights import police_blink, shift_update, blanks
from stream import init_streaming_server

leftMotor = Motor(12, 13)
rightMotor = Motor(25, 21)
lightsOn = False

PORT = 1488


def debounce(wait_time):

    def decorator(function):
        def debounced(*args, **kwargs):
            def call_function():
                debounced._timer = None
                return function(*args, **kwargs)

            if debounced._timer is not None:
                debounced._timer.cancel()

            debounced._timer = threading.Timer(wait_time, call_function)
            debounced._timer.start()

        debounced._timer = None
        return debounced

    return decorator


@debounce(1)
def idle():
    leftMotor.stop()
    rightMotor.stop()


def enable_lights():
    global lightsOn

    lightsOn = True

    while lightsOn:

        try:
            police_blink()
        except KeyboardInterrupt:
            shift_update([0, 0, 0] + blanks)
            break

    shift_update([0, 0, 0] + blanks)


def disable_lights():
    global lightsOn

    lightsOn = False
    shift_update([0, 0, 0] + blanks)


def awakening():
    leftMotor.forward(1)
    time.sleep(.5)
    leftMotor.backward(1)
    time.sleep(.5)
    leftMotor.stop()
    rightMotor.forward(1)
    time.sleep(.5)
    rightMotor.backward(1)
    time.sleep(.5)
    rightMotor.stop()


async def echo(websocket):
    async for message in websocket:
        idle()

        payload = json.loads(message)
        left = payload.get("left", 0)
        right = payload.get("right", 0)
        light = payload.get("light", None)

        if left > 0:
            leftMotor.forward(left)
        elif left < 0:
            leftMotor.backward(abs(left))
        else:
            leftMotor.stop()

        if right > 0:
            rightMotor.forward(right)
        elif right < 0:
            rightMotor.backward(abs(right))
        else:
            rightMotor.stop()

        if light == 1:
            #t1 = threading.Thread(target=enable_lights)
            t1 = threading.Thread(target=buzz)
            t1.setDaemon(True)
            t1.start()

        elif light == 0:
            disable_lights()


async def main():
    async with websockets.serve(echo, "", PORT):
        awakening()
        init_streaming_server()
        disable_lights()
        await asyncio.Future()


asyncio.run(main())
