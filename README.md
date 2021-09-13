# rocket-pi

Ever want to capture video from a model rocket? With the new low-cost Raspberry Pi Zero, now you can! 

Properly configured, this script will run when you boot your Pi. If it detects that the camera is attached, it will 
turn on the LED attached to GPIO pin 17 and begin recording. It will record for 2 minutes, stop capture and power off the Pi.

The initial version of this project just captured video and stored it in the Videos folder of the current user. With this verison,
GPS data is captured as well.

We weren't able to get gpsd to work reliably, so we just capture the raw NMEA data from the serial port which is why the script 
must be run via ```sudo```.

## Parts list

-  [Adafruit Ultimate GPS Breakout - 66 channel w/10 Hz updates - Version 3](https://www.adafruit.com/products/746)
-  [PowerBoost 500 Basic - 5V USB Boost @ 500mA from 1.8V+](https://www.adafruit.com/products/1903)
-  [Raspberry Pi Camera Board v2 - 8 Megapixels](https://www.adafruit.com/products/3099)
-  [Raspberry Pi Zero v1.3 Camera Cable](https://www.adafruit.com/products/3157)
-  [Lithium Ion Battery - 3.7v 2000mAh](https://www.adafruit.com/products/2011)
-  [Raspberry Pi Zero - Version v1.3](https://www.adafruit.com/products/2885)

## Configuration
Clone this repo on your Pi.
Edit your .bashrc to run rocket.py. This should be the last line -- and you'll need to run it as root to access the serial port:

```sudo rocket-pi/rocket.pi``` 


## Amateur-ish Fritzing Diagrams
![schematic](https://github.com/paquettej/rocket-pi/blob/main/images/RocketPi_schematic.png)

