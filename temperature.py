import time
import signal
from threading import Event

import RPi.GPIO as GPIO
import Adafruit_DHT

from tm1637 import TM1637, BRIGHT_DARKEST

__author__ = "Evgeny Goncharov"

run_service = Event()
run_service.set()


def handler(signum, frame):
    run_service.clear()
    print("Signal to stop container {}".format(signum))


signal.signal(signal.SIGTERM, handler)

CLK = 6
DIO = 5

DHT11_pin = 16

Display = TM1637(CLK, DIO, BRIGHT_DARKEST)

F0 = 25.
N = 10.
ALPHA = 2 / (N + 1)
BETA = 1 - ALPHA


def EMA(temperature, ema_old):
    return ALPHA * temperature + BETA * ema_old


while run_service.is_set():
    hmd, tmp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT11_pin)

    if hmd and tmp:
        f = EMA(tmp, F0)
        break
    else:
        time.sleep(1)


while run_service.is_set():
    hmd, tmp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT11_pin)

    if hmd and tmp:
        f = EMA(tmp, f)

        # print("f0: ", f0, "temperature: ", tmp, " humidity: ", hmd)

        temperature = int(round(f))

        d0 = int(temperature / 10)
        d1 = temperature % 10

        Display.show([d0, d1, 16, 12])

        # Display.show_double_point(second % 2)

    try:
        time.sleep(5)
    except:
        pass

Display.set_brightness(0)
Display.clear()

GPIO.cleanup([CLK, DIO, DHT11_pin])
