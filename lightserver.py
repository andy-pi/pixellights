'''
Flask server for Raspberry Pi Google Activated lights
'''

from flask import Flask
import adafruit_ws2801
import board
from config import *
app = Flask(__name__)

leds = adafruit_ws2801.WS2801(board.SCK, board.MOSI, 12, brightness=1)

@app.route('/lights/<colour>/<password>')
def lights(colour, password):
    '''
    Sets WS2801 pixel to specified colour
    '''

    if password not in PASSWORD:
        return 404

    if colour == "off":
        leds.fill((255, 255, 255))

    elif colour == "warm":
        leds.fill((255, 214, 170))

    elif colour == "red":
        leds.fill((255, 0, 0))

    elif colour == "blue":
        leds.fill((0, 0, 255))

    elif colour == "green":
        leds.fill((0, 255,0))

    elif colour == "purple":
        leds.fill((170, 0, 255))

    elif colour == "orange":
        leds.fill((255, 128, 0))

    elif colour == "yellow":
        leds.fill((255, 255, 0))

    else:
        leds.fill((0, 0, 0))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)#, debug=True)
