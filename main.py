# Imports
from machine import Pin, I2C, PWM, reset
from ssd1306 import SSD1306_I2C
from neopixel import NeoPixel
import time
import random

global options
global choice

red = 255,0,0
green = 0,255,0
blue = 0,0,255
yellow = 255,255,0
pink = 255,20,147

# Set Up display
i2c=I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

strip = NeoPixel(Pin(28), 15)
strip.fill((0,0,0))
strip.write()

left = Pin(18, Pin.IN, Pin.PULL_DOWN)
middle = Pin(19, Pin.IN, Pin.PULL_DOWN)
right = Pin(20, Pin.IN, Pin.PULL_DOWN)

board_LED = Pin(25, Pin.OUT)

buzzer = PWM(Pin(15))
buzzer.freq(1000)
buzzer.duty_u16(0)

options = ["Millsted", "Skinner", "Wright", "Rumph", "Piecha"]
choice = 0

time.sleep(1)
display = SSD1306_I2C(128, 32, i2c)
display.fill(0)

def main():
    
    board_LED.value(0)
    
    display.fill(0)
    display.text("Who is the best", 0, 0)
    display.text("Able Cadet ?", 0, 11)
    blink(["Who is the best", "Able Cadet ?", option(choice)], (36, 22), 0.1)
    display.show()

def option(num):
    num = max(0, num)
    num = min(num, 4)
    
    return options[num]

def events():
    l, m, r = False, False, False
    
    if left.value() == 1:
        l = True
    if middle.value() == 1:
        m = True
    if right.value() == 1:
        r = True
    
    return l, m, r

def rainbow():
    delay = 0.01
    inverse = False
    for i in range(2):
        inverse = not inverse
        if inverse:
            for x in range(255, 1, -1):
                for y in range(15):
                    strip[y] = (255*x,20*x,147*x)
                    strip.write()
                    time.sleep(delay * i)
        else:
            print("SWAP")
            for x in range(1, 255, 1):
                for y in range(15):
                    strip[y] = (255*x,20*x,147*x)
                    strip.write()
                    time.sleep(delay * i)
        

def enter():
    o = option(choice)
    
    display.fill(0)
    
    if o == "Millsted":
        display.text("Correct", 38, 11)
        display.show()
        time.sleep(3)
        # rainbow()
        strip.fill((0, 0, 0))
        strip.write()
        display.poweroff()
        reset()
    else:
        display.text("Wrong", 38, 11)
        display.show()
        for i in range(15):
            strip[i] = (255, 0, 0)
            strip.write()
            time.sleep(0.01)
        buzzer.duty_u16(10000)
        time.sleep(3)
        buzzer.duty_u16(0)
        for i in range(14, 0, -1):
            strip[i] = (0, 0, 0)
            strip.write()
            time.sleep(0.01)
        strip.fill((0, 0, 0))
        strip.write()

def blink(text, pos, delay):
    global choice
    x, y = pos
    while True:
        display.text(text[0], 0, 0)
        display.text(text[1], 0, 11)
        
        display.text(text[2], x, y)
        display.show()
        time.sleep(delay)
        
        display.fill(0)
        
        display.text(text[0], 0, 0)
        display.text(text[1], 0, 11)
        
        display.show()
        time.sleep(delay)
        
        l, m, r = events()
        
        if l:
            choice -= 1
        elif m:
            break
        elif r:
            choice += 1
        else:
            text[2] = option(choice)
    enter()
main()

