import time

import RPi.GPIO as GPIO

__author__ = "Evgeny Goncharov"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

ADDR_AUTO = 0x40  # 64
ADDR_FIXED = 0x44  # 68
START_ADDR = 0xC0  # 192

BRIGHT_DARKEST = 0
BRIGHT_TYPICAL = 2
BRIGHT_HIGHEST = 7

digit_to_segment = (
    0b0111111,  # 0
    0b0000110,  # 1
    0b1011011,  # 2
    0b1001111,  # 3
    0b1100110,  # 4
    0b1101101,  # 5
    0b1111101,  # 6
    0b0000111,  # 7
    0b1111111,  # 8
    0b1101111,  # 9
    0b1110111,  # A
    0b1111100,  # b
    0b0111001,  # C
    0b1011110,  # d
    0b1111001,  # E
    0b1110001,  # F
    0b1100011,  # degree
    0b1000000,  # minus
    0b0000000,  # nothing
)


class TM1637():
    def __init__(self, clk, dio, brightness=0):
        self._clk_pin = clk
        self._data_pin = dio
        self._brightness = brightness
        self._double_point = False
        self._current_data = [0, 0, 0, 0]

        GPIO.setup(self._clk_pin, GPIO.OUT)
        GPIO.setup(self._data_pin, GPIO.OUT)

    def clear(self):
        self._double_point = False
        self.show((18, 18, 18, 18))

    def show(self, data):
        self._current_data = data
        self.start()
        self.write_byte(ADDR_AUTO)
        self.stop()
        self.start()
        self.write_byte(START_ADDR)
        for i in data:
            if self._double_point:
                self.write_byte(digit_to_segment[i] + 0x80)
            else:
                self.write_byte(digit_to_segment[i])
        self.stop()
        self.start()
        self.write_byte(0x88 + self._brightness)
        self.stop()

    def set_brightness(self, brightness):
        if brightness >= 7:
            brightness = 7
        elif brightness < 0:
            brightness = 0

        if self._brightness != brightness:
            self._brightness = brightness
            self.show(self._current_data)

    def show_double_point(self, on):
        self._double_point = on
        self.show(self._current_data)

    def write_byte(self, data):
        for i in range(8):
            GPIO.output(self._clk_pin, GPIO.LOW)
            if data & 0x01:
                GPIO.output(self._data_pin, GPIO.HIGH)
            else:
                GPIO.output(self._data_pin, GPIO.LOW)
            data = data >> 1
            GPIO.output(self._clk_pin, GPIO.HIGH)

        # wait for ACK
        GPIO.output(self._clk_pin, GPIO.LOW)
        GPIO.output(self._data_pin, GPIO.HIGH)
        GPIO.output(self._clk_pin, GPIO.HIGH)
        GPIO.setup(self._data_pin, GPIO.IN)

        while GPIO.input(self._data_pin):
            time.sleep(0.001)
            if GPIO.input(self._data_pin):
                GPIO.setup(self._data_pin, GPIO.OUT)
                GPIO.output(self._data_pin, GPIO.LOW)
                GPIO.setup(self._data_pin, GPIO.IN)

        GPIO.setup(self._data_pin, GPIO.OUT)

    def start(self):
        GPIO.output(self._clk_pin, GPIO.HIGH)  # send start signal to TM1637
        GPIO.output(self._data_pin, GPIO.HIGH)
        GPIO.output(self._data_pin, GPIO.LOW)
        GPIO.output(self._clk_pin, GPIO.LOW)

    def stop(self):
        GPIO.output(self._clk_pin, GPIO.LOW)
        GPIO.output(self._data_pin, GPIO.LOW)
        GPIO.output(self._clk_pin, GPIO.HIGH)
        GPIO.output(self._data_pin, GPIO.HIGH)


if __name__ == "__main__":
    CLK = 18
    DIO = 25

    Display = TM1637(CLK, DIO, BRIGHT_DARKEST)

    for i in range(10):
        current_time = (i, i, i, i)

        Display.show(current_time)
        Display.show_double_point(i % 2)

        try:
            time.sleep(1)
        except:
            pass

    Display.set_brightness(0)
    Display.clear()

    GPIO.cleanup([CLK, DIO])

    '''
    (0, 191, '0b10111111')
    (1, 134, '0b10000110')
    (2, 219, '0b11011011')
    (3, 207, '0b11001111')
    (4, 230, '0b11100110')
    (5, 237, '0b11101101')
    (6, 253, '0b11111101')
    (7, 135, '0b10000111')
    (8, 255, '0b11111111')
    (9, 239, '0b11101111')
    '''
