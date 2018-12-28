from flask import Flask
from AndyPiPixelLights import AndyPiPixelLights
from config import *
app = Flask(__name__)

pixellights = AndyPiPixelLights(10)

@app.route('/lights/<colour>/<password>')
def lights(colour, password):
    '''
    Sets WS2801 pixel to specified colour
    '''
    
    if password not in PASSWORD:
        return 404
    
    if colour =="on":
        pixellights.lightall(0, 0, 0)
    
    elif colour =="off":
        pixellights.lightall(255, 255, 255)
        
    elif colour =="warm":
        pixellights.lightall(255, 214, 170)
    
    elif colour =="red":
        pixellights.lightall(255, 0, 0)
        
    elif colour =="blue":
        pixellights.lightall(0, 0, 255)
        
    elif colour =="green":
        pixellights.lightall(0, 255, 0)
        
    elif colour =="purple":
        pixellights.lightall(170, 0, 255)
       
    elif colour =="orange":
        pixellights.lightall(255, 128, 0)
        
    elif colour =="yellow":  
        pixellights.lightall(255, 255, 0)
        
    else:   
        rainbowCycle(0.00)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)#, debug=True)