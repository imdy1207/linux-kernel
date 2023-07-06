import RPi.GPIO as rg
import time

rg.setmode(rg.BCM)

ledPlusPins = [27, 8]

rg.setup(ledPlusPins, rg.OUT)

try:
    while True:
        for i in range(len(ledPlusPins)):
            rg.output(ledPlusPins[i], rg.LOW) if i%2 == 0 else rg.output(ledPlusPins[i], rg.HIGH)
        time.sleep(1)

        for i in range(len(ledPlusPins)):
            rg.output(ledPlusPins[i], rg.HIGH) if i%2 == 0 else rg.output(ledPlusPins[i], rg.LOW)
        time.sleep(1)

except KeyboardInterrupt:
    rg.cleanup()
