import RPi.GPIO as rg
from datetime import datetime
import time

led_pins = [27, 22, 23, 24]

rg.setmode(rg.BCM)
rg.setup(led_pins, rg.OUT)

try:
    while True:
        current_time = datetime.now().second 
        
        for i, pin in enumerate(led_pins):
            rg.output(pin, (current_time%16) >> i & 1)
        
        time.sleep(1)

except KeyboardInterrupt:
    rg.cleanup()
