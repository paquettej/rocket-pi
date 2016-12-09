#!/usr/bin/python

# External module imports
import time
import datetime
import os
import subprocess
import serial
import threading

# rPi support 
import RPi.GPIO as GPIO
import picamera

# Pin Definitons:
ledPin = 17 # Broadcom pin 23 (P1 pin 16)
GPIO_Configured = False
data_file_name = None

def setup():
    # Pin Setup:
    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
    # Initial state for LEDs:
    GPIO.output(ledPin, GPIO.LOW)
    GPIO_Configured = True


def teardown():
    # release our GPIO config
    if GPIO_Configured:
        GPIO.cleanup() # cleanup all GPIO

def poweroff():
    command = "/usr/bin/sudo /sbin/shutdown  now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

def ledOn():
    GPIO.output(ledPin, GPIO.HIGH)

def ledOff():
    GPIO.output(ledPin, GPIO.LOW)

def isCameraConnected():
    # check if camera connected
    print("checking for camera")
    cmd = "/usr/bin/vcgencmd get_camera"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    if "detected=1" in output:
        return True
    return False


def getDataFolder():
    directory = '/home/pi/Videos/' + time.strftime("%Y-%m-%d")
    print("Saving videos to " + directory)
    if not os.path.exists(directory):
        print("Making folder " + directory)
        os.makedirs(directory)
    return directory


def acquire():
    with open(data_file_name, "ab") as datafile:
        with serial.Serial("/dev/ttyAMA0", 115200) as port:
            while True:
                try:
                    line = port.readline()
                    datafile.write(line)
                    datafile.flush()
                except Exception as e:
                    continue

try:
    if not isCameraConnected():
        exit(0)

    setup()

    # make folder based on datestamp
    directory = getDataFolder()

    current_timestamp = time.strftime("%H-%M-%S")
    video_file = directory + "/flight-" + current_timestamp + ".h264"
    print("Video file is " + video_file)

    gps_file = directory +  "/flight-" + current_timestamp + ".gps.csv"
    print("GPS data file is " + gps_file)
    data_file_name = gps_file

    # turn on led
    ledOn()

    acquire_data = threading.Event()
    # start GPS capture
    acquisition_thread = threading.Thread(name='gps_acquisition', target=acquire)
    acquisition_thread.setDaemon(True)

    acquisition_thread.start()
    
    # capture video for 2 minutes to that folder
    with picamera.PiCamera() as camera:
        # Camera warm-up time
        time.sleep(2)
        camera.start_recording(video_file, format='h264', );
        print("Capture started")
        camera.wait_recording(2 * 60)
        # stop capture
        camera.stop_recording()
        print("Capture complete")

    # turn off led
    ledOff()

    # power off the system
    print("Capture complete, powering down")
    poweroff()
finally:
    teardown()
