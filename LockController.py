import RPi.GPIO as gpio
import time
'''
A controller for the lock mechanism through GPIO
Makes it east to assert individual locks for a brief period of time
'''
#gpio.setwarnings(False)

gpio.setmode(gpio.BCM)

# A relation between locks and GPIO pins in the form LOCK:GPIO_PIN
pins = {1:2, 2:4, 3:17, 4:22, 5:10, 6:11, 7:5, 8:13}

# Initialize each pin to output
for pin in list(pins.keys()):
    gpio.setup(pins[pin], gpio.OUT)

# Helper methods to assert individual pins
def assert1(pin):
    gpio.output(pins[pin], gpio.HIGH)

def assert0(pin):
    gpio.output(pins[pin], gpio.LOW)

# Sets all working pins to 0
def lockAll():
    for pin in list(pins.keys()):
        assert0(pin)

# unlocks a given lock for 4 seconds
def unlock(lock):
    assert1(lock)
    time.sleep(4)
    lockAll()

# power-cycles all locks on startup
for pin in list(pins.keys()):
        assert1(pin)
lockAll()
