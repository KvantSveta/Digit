import time
import signal
from threading import Event
from subprocess import check_output

import RPi.GPIO as GPIO

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

Display = TM1637(CLK, DIO, BRIGHT_DARKEST)

while run_service.is_set():
    output = check_output(["cat", "/sys/bus/w1/devices/28-05170143ccff/w1_slave"])

    # output = '92 01 4b 46 7f ff 0c 10 b5 : crc=b5 YES\n92 01 4b 46 7f ff 0c 10 b5 t=25125\n'
    output = output.decode()

    # b = 't=25125'
    output = output.split()[-1]

    # temp = '25125'
    temp = output.split("=")[1]

    # digit_temp = 25.0
    digit_temp = round(int(temp) / 1000)

    if digit_temp:
        # d0 = 2
        d0 = int(digit_temp / 10)
        # d1 = 5
        d1 = int(digit_temp % 10)

        Display.show([d0, d1, 16, 12])

    try:
        time.sleep(5)
    except:
        pass

Display.set_brightness(0)
Display.clear()

GPIO.cleanup([CLK, DIO])
