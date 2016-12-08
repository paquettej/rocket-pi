from gps import *
import time
import threading
import math
import csv

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
            self.log_data()

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

    def waiting_for_fix(self):
        return math.isnan(self.fix.latitude) or self.fix.latitude = 0.0

    def log_data(self):
        f = self.fix
        current_data = [f.latitude, f.longitude, f.time, f.altitude, f.eps, f.epx, f.epv, f.ept, f.speed, f.climb,f.track,f.mode]
        with open(self.datafile, "ab") as myfile:
            writer = csv.writer(myfile)
            writer.writerow(current_data)

    def set_datafile(self,file_name):
        self.datafile = file_name
        self.write_data_headers()

    def write_data_headers(self):
        with open(self.datafile, "w") as log:
            log.write("latitude,longitude,time utc,altitude (m),eps,epx,epv,ept,speed (m/s),climb,track,mode\n")


