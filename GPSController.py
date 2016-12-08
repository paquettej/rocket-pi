from gps import *
import time
import threading
import math

class GpsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.running = False
        self.datafile = ""

    def run(self):
        self.running = True
        while self.running:
            # grab EACH set of gpsd info to clear the buffer
            self.gpsd.next()

    def stopController(self):
        self.running = False

    @property
    def fix(self):
        return self.gpsd.fix

    @property
    def utc(self):
        return self.gpsd.utc

    @property
    def satellites(self):
        return self.gpsd.satellites

    @property
    def waiting_for_fix():
        return not self.fix.latitude

    def log_data():
        f = gpsc.fix
        current_data = ""
        current_data = f.latitude + ","
        current_data = f.longitude + ","
        current_data = f.utc + ","
        current_data = f.time + ","
        current_data = f.altitude + ","
        current_data = f.eps + ","
        current_data = f.epx + ","
        current_data = f.epv + ","
        current_data = f.ept + ","
        current_data = f.speed + ","
        current_data = f.climb + ","
        current_data = f.track + ","
        current_data = f.mode
        with open(self.datafile, "a") as myfile:            
            myfile.write(current_data)

    def set_datafile(file_name):
        self.datafile = file_name
        self.write_data_headers()

    def write_data_headers():
        with open(self.datafile) as log:
            log.write("latitude,longitude,time utc,altitude (m),eps,epx,epv,ept,speed (m/s),climb,track,mode,sats ")


