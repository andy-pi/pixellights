'''
WS2801 SPI control class for Raspberry Pi
Author:   AndyPi (http://andypi.co.uk/)
Based on: Adafruit https://raw.githubusercontent.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/master/Adafruit_LEDpixels/Adafruit_LEDpixels.py
Hardware: WS2801 pixels, CLOCK=RPi23; Data=RPi19, GND=RpiGND, +5v=Rpi+5v
'''

import time
import sys
import RPi.GPIO as GPIO

class AndyPiPixelLights():

    def __init__(self, pixelcount=1):
        '''
        initialize class with number of pixels
        '''
        GPIO.setmode(GPIO.BCM)
        self.ledpixels = [0] * pixelcount

    def writestrip(self, pixels):
        '''
        Send data for the whole LED strip via SPI
        '''
        try:
            spidev = open("/dev/spidev0.0", "bw")
            for pixel in pixels:
                spidev.write(chr((pixel >> 16) & 0xFF).encode('latin-1'))
                spidev.write(chr((pixel >> 8) & 0xFF).encode('latin-1'))
                spidev.write(chr((pixel >> 0) & 0xFF).encode('latin-1'))
        except ValueError:
            spidev = open("/dev/spidev0.0", "w")
            for pixel in pixels:
                spidev.write(chr((pixel >> 16) & 0xFF))
                spidev.write(chr((pixel >> 8) & 0xFF))
                spidev.write(chr((pixel >> 0) & 0xFF))
        spidev.close()
        time.sleep(0.002)

    def color(self, red, green, blue):
        '''
        Convert RGB values to correct format for SPI write
        '''
        return ((int(red) & 0xFF) << 16) | ((int(green) & 0xFF) << 8) | (int(blue) & 0xFF)

    def setpixelcolor(self, pixels, n, color):
        '''
        Sets the colour of a pixel
        '''
        if n >= len(pixels):
            return
        pixels[n] = color

    def colorwipe(self, pixels, color, delay):
        '''
        Wipes the specified colour along the strip
        '''
        for pixel in pixels:
            self.setpixelcolor(pixels, pixel, color)
            self.writestrip(pixels)
            time.sleep(delay)

    def wheel(self, wheelpos):
        '''
        Helper functions to chose colour in the rainbow
        '''
        if wheelpos < 85:
            return self.color(wheelpos * 3, 255 - wheelpos * 3, 0)
        elif wheelpos < 170:
            wheelpos -= 85
            return self.color(255 - wheelpos * 3, 0, wheelpos * 3)
        else:
            wheelpos -= 170
            return self.color(0, wheelpos * 3, 255 - wheelpos * 3)

    def rainbowcycle(self, wait):
        '''
        Cycles through a rainbow of colours
        '''
        for j in range(256):  # one cycle of all 256 colors in the wheel
            for i in range(len(self.ledpixels)):
                # tricky math! we use each pixel as a fraction of the full 96-color wheel
                # (thats the i / strip.numPixels() part)
                # Then add in j which makes the colors go around per pixel
                # the % 96 is to make the wheel cycle around
                self.setpixelcolor(self.ledpixels, i, self.wheel(((i * 256 / len(self.ledpixels)) + j) % 256))
            self.writestrip(self.ledpixels)
            time.sleep(wait)

    def clearall(self, pixels):
        '''
        Turns all pixels off
        '''
        for i in range(len(pixels)):
            self.setpixelcolor(pixels, i, self.color(0, 0, 0))
            self.writestrip(pixels)

    def lightall(self, red, green, blue):
        '''
        Light all pixels specified RGB colour
        '''
        for i in range(len(self.ledpixels)):
            self.setpixelcolor(self.ledpixels, i, self.color(red, green, blue))
            self.writestrip(self.ledpixels)

    def main(self):
        '''
        Demo
        '''
        try:
            self.colorwipe(self.ledpixels, self.color(255, 0, 0), 0.05)
            self.colorwipe(self.ledpixels, self.color(0, 255, 0), 0.05)
            self.colorwipe(self.ledpixels, self.color(0, 0, 255), 0.05)
            self.rainbowcycle(0.00)
            self.clearall(self.ledpixels)

        except KeyboardInterrupt:
            self.clearall(self.ledpixels)
            sys.exit(0)


if __name__ == '__main__':
    LEDS = AndyPiPixelLights()
    LEDS.main()
