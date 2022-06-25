#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# libraries
from threading import Thread
from paho import mqtt
from dotenv import load_dotenv
import time
import os
import RPi.GPIO as GPIO
# import paho.mqtt.client as paho
import paho.mqtt.client as paho
from paho import mqtt

load_dotenv()

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
    
    def move(self):
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
        self.direction = "stop"

    def quit(self):
        self._running = False

    def run(self):
        while self._running:
            if(self.direction != "stop"):
                self.move()
            time.sleep(0.002)
        for pin in self.stepPins:
            GPIO.output(pin, False)
        GPIO.cleanup()


class MyMQTTClass(paho.Client):

    def set_stepper_class(self, stepperMotorClass):
        self._stepperMotorClass = stepperMotorClass

    def on_connect(self, mqttc, obj, flags, rc):
        print("rc: "+str(rc))

    def on_connect_fail(self, mqttc, obj):
        print("Connect failed")

    def on_message(self, mqttc, obj, msg):
        print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
        command = str(msg.payload)
        print(command)
        if (command == "b'forward'"):
            self._stepperMotorClass.moveForward()
        elif (command == "b'backward'"):
            self._stepperMotorClass.moveBackward()
        elif (command == "b'stop'"):
            self._stepperMotorClass.stop()

    def quit(self):
        self.loop_stop()

    def run(self):
        self.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
        self.username_pw_set(os.getenv("MQTT_BROKER_USERNAME"), os.getenv("MQTT_BROKER_PASSWORD"))
        self.connect(os.getenv("MQTT_BROKER_HOST"), int(os.getenv("MQTT_BROKER_PORT")))
        self.subscribe("testtopic/1", 0)

        self.loop_start()

        # rc = 0
        # while rc == 0:
        #     rc = self.loop()
        # return rc

s = StepperMotor()
m = MyMQTTClass()
m.set_stepper_class(s)
st = Thread(target=s.run)
mt = Thread(target=m.run)
st.start()
mt.start()

running = True
while running:
    command = input("command [f/b/s/q]: ")
    if command == "f":
        s.moveForward()
    elif command == "b":
        s.moveBackward()
    elif command == "s":
        s.stop()
    elif command == "q":
        s.quit()
        m.quit()
        running = False