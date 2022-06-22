#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# libraries
import time
import RPi.GPIO as GPIO
from threading import Thread

class StepperMotor:
    def __init__(self):
        self._running = True
        self.direction = "forward"
        # Use BCM GPIO references
        # Instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)

        # Define GPIO signals to use Pins 18,22,24,26 GPIO24,GPIO25,GPIO8,GPIO7
        self.stepPins = [24,25,8,7]
        # Set all pins as output
        for pin in self.stepPins:
            print("Setup pins {}".format(pin))
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)

        # Define some settings
        self.waitTime = 0.01

        # Define simple sequence
        StepCount1 = 4
        Seq1 = [[ True, False, False, False],[False,  True, False, False],[False, False, True,  False],[False, False, False, True]]
        # Define advanced half-step sequence
        StepCount2 = 8
        Seq2 = [[  True, False, False, False ],[  True,  True, False, False ],[ False,  True, False, False ],[ False,  True,  True, False ],[ False, False,  True, False ],[ False, False,  True,  True ],[ False, False, False,  True ],[  True, False, False,  True ]]
        # Choose a sequence to use
        self.seq = Seq2
        self.stepCount = StepCount2

        self.step = 0
    
    def stepForward(self):
        for pin in range(4):
            GPIO.output(self.stepPins[pin], self.seq[self.step][pin])
        if self.direction == "forward":
            self.step = (self.step + 1) % self.stepCount
        else:
            self.step = (self.step - 1) % self.stepCount


    def moveForward(self):
        self.direction = "forward"
    
    def moveBackward(self):
        self.direction = "backward"

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            self.stepForward()
            time.sleep(0.002)
        for pin in self.stepPins:
            GPIO.output(pin, False)
        GPIO.cleanup()

s = StepperMotor()
t = Thread(target=s.run)
t.start()
running = True
while running:
    command = input("command [f/b/s]: ")
    if command == "f":
            s.moveForward()
    elif command == "b":
            s.moveBackward()
    elif command == "s":
            s.stop()
            running = False
