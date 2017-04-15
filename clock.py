import time
import signal
from datetime import datetime
from threading import Event

import RPi.GPIO as GPIO

from tm1637 import TM1637

__author__ = "Evgeny Goncharov"

run_service = Event()
run_service.set()


def handler(signum, frame):
    run_service.clear()
    print("Сигнал для остановки контейнера {}".format(signum))


signal.signal(signal.SIGTERM, handler)

# CLK -> GPIO23 (Pin 16)
# Di0 -> GPIO24 (Pin 18)

CLK = 23
DIO = 24

Display = TM1637(CLK, DIO, TM1637.BRIGHT_HIGHEST)


while run_service.is_set():
    date = datetime.now()

    hour = date.hour
    minute = date.minute
    second = date.second

    currenttime = [int(hour / 10), hour % 10, int(minute / 10), minute % 10]

    Display.show(currenttime)
    Display.show_double_point(second % 2)

    try:
        time.sleep(1)
    except:
        pass

Display.set_brightness(0)
Display.clear()

GPIO.cleanup([CLK, DIO])
