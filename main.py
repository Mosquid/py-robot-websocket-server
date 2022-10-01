import asyncio
import time
import websockets
from gpiozero import Motor
import json
import threading

leftMotor = Motor(12, 13)
rightMotor = Motor(25, 21)

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
        left = payload["left"]
        right = payload["right"]

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


async def main():
    async with websockets.serve(echo, "", PORT):
        awakening()
        await asyncio.Future()


asyncio.run(main())
