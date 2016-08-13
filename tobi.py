#try:
from __future__ import print_function
from nanpy import (ArduinoApi, SerialManager)
from nanpy.arduinotree import ArduinoTree
from nanpy.PCF8574 import PCF8574
from time import sleep
import threading
import time, threading




connection = SerialManager(sleep_after_connect=2)
connection.open()
a = ArduinoApi(connection = connection)
w = ArduinoTree(connection=connection)
MOTOR_EXP_1 = 0x38
MOTOR_EXP_2 = 0x39
pcf_1 = PCF8574(w.wire,MOTOR_EXP_1)
pcf_2 = PCF8574(w.wire,MOTOR_EXP_2)

print ("SUCCESS : Connection to Arduino secure")

#except :
#print ("ERROR : Check if the Arduino has been connected and Nanpy has been loaded onto it")
#except:
#print("ERROR: Make sure the Nanpy folder is included in main directory")
    
class tobi:
    global a,b,pcf_1,pcf_2
        
    encoder = [0,1,2,3,4,5]
    bit_1=0b00000000
    bit_2=0b00000000
 #todo replace bit with __bit to prevent exteral editing 

    def __init__(self):
        pcf_1.write8(tobi.bit_1)
        print("SUCCESS : tobi initialized")

    def enable(self):
        """Sets the robot in Tobi Mode, enabling and disabling pins"""
        # set PWM pins to OUTPUT
        pwm = [4,5,6,11,12,13]
        for i in range(0,6):
            a.pinMode(pwm[i], a.OUTPUT)

        # set Encoder pins to INPUT
        for i in range(0,6):
            a.pinMode(i,a.INPUT)

        self.__setEncoder()
        print("SUCCESS : System in Tobi Mode")        
        
    def setMotor(self,motor,direction):
        """motors range from 1-6
        direction 1 -> front  -1 -> back else -> nothing
        uses PCF io expander and bit shifts"""
        
        if not(motor>0 and motor < 7):
            print ("wrong motor chosen")
            return
        
        if (direction == 1):
            tobi.bit_1 |= (1<<motor-1)  #because of circuitry , check eagle
           
        elif (direction == -1):
            tobi.bit_1 &= ~(1<<(motor-1))

        else :
            print ("wrong command")

        pcf_1.write8(tobi.bit_1)

    def powerAxis(self, axis, state):
        """turn motor axis on/off (1 -> M1-M2 ,2 -> M3-M4, 3-> M5-M6
        works on enable pins for motor driver"""
        if (axis == 1):
            if state == 1:
                tobi.bit_1 |= (1<<6)
            elif state == 0 :
                tobi.bit_1 &= ~(1<<6)
            pcf_1.write8(tobi.bit_1)            

        elif (axis == 2):
            if state == 1:
                tobi.bit_1 |= (1<<7)
            elif state == 0 :
                tobi.bit_1 &= ~(1<<7)
            pcf_1.write8(tobi.bit_1)

        elif (axis == 3):
            if state == 1:
                tobi.bit_2 |= (1<<0)
            elif state == 0 :
                tobi.bit_2 &= ~(1<<0)
            pcf_2.write8(tobi.bit_2)


        else :
            print("ERROR : Incorrect command")

    def tprint(self):
        """prints information about internal class"""
        print ("Bit 1 =  %s" % bin(tobi.bit_1))
        print ("Bit 2 = " , end ="")
        print(bin(tobi.bit_2))
        for i in range(0,6):
            print ("Encoder %d = %d" %(i,tobi.encoder[i]))
            pass
            

    def getEncoder(self,leg):
        """displays encoder values for a single motor"""
        print (tobi.encoder[leg])

    def __setEncoder(self):
        for i in range(0,6):
            tobi.encoder[i] = a.analogRead(i)
        threading.Timer(0.05,self.__setEncoder).start()



                
        

        
    
    
