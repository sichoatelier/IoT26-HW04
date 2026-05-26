'''
Adapted excerpt from Getting Started with Raspberry Pi by Matt Richardson
Modified by Rui Santos
Complete project details: https://randomnerdtutorials.com

Ported to gpiozero for Raspberry Pi 5 compatibility.
'''

from flask import Flask, render_template, request
from gpiozero import LED  # Import LED object to control OUT pins

app = Flask(__name__)

# Map gpiozero LED objects to a dictionary for easier management.
# Hardware pin configuration (OUT) and initial state (LOW) are automatically set upon initialization.
pins = {
   23 : {'name' : 'GPIO 23', 'device' : LED(23)},
   24 : {'name' : 'GPIO 24', 'device' : LED(24)}
}

@app.route("/")
def main():
   # Construct the state data to be passed to the template (main.html)
   template_pins = {}
   for pin in pins:
      template_pins[pin] = {
         'name': pins[pin]['name'],
         # pins[pin]['device'].value returns 1 (True) if on, and 0 (False) if off.
         'state': pins[pin]['device'].value 
      }
      
   templateData = {
      'pins' : template_pins
   }
   return render_template('main.html', **templateData)

@app.route("/<changePin>/<action>")
def action(changePin, action):
   changePin = int(changePin)
   deviceName = pins[changePin]['name']
   
   # Retrieve the corresponding gpiozero device object
   led_device = pins[changePin]['device']

   if action == "on":
      led_device.on()  # Set the pin state to HIGH
      message = "Turned " + deviceName + " on."
   elif action == "off":
      led_device.off() # Set the pin state to LOW
      message = "Turned " + deviceName + " off."

   # Re-assemble the dictionary with the latest states of all pins
   template_pins = {}
   for pin in pins:
      template_pins[pin] = {
         'name': pins[pin]['name'],
         'state': pins[pin]['device'].value
      }

   templateData = {
      'pins' : template_pins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   # Port 80 requires administrative privileges, so 'sudo' is mandatory.
   app.run(host='0.0.0.0', port=80, debug=False)
