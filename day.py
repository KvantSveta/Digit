import time
import signal
from datetime import datetime
from threading import Event

import RPi.GPIO as GPIO

from tm1637 import TM1637, BRIGHT_DARKEST

__author__ = "Evgeny Goncharov"

run_service = Event()
run_service.set()


def handler(signum, frame):
    run_service.clear()
    print("Signal to stop container {}".format(signum))


signal.signal(signal.SIGTERM, handler)

CLK = 18
DIO = 25

Display = TM1637(CLK, DIO, BRIGHT_DARKEST)


while run_service.is_set():
    date = datetime.now()

    day = date.day
    month = date.month

    Display.show([int(day / 10), day % 10, int(month / 10), month % 10])

    Display.show_double_point(True)

    try:
        time.sleep(1)
    except:
        pass

Display.set_brightness(0)
Display.clear()

GPIO.cleanup([CLK, DIO])
