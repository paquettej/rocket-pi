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
    def waiting_for_fix
        return not self.fix.latitude

    def log_data()
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


if __name__ == '__main__':
    # create the controller
    gpsc = GpsController()
    try:
        # start controller
        gpsc.start()
        while True:
            print "latitude ", gpsc.fix.latitude
            print "longitude ", gpsc.fix.longitude
            print "time utc ", gpsc.utc, " + ", gpsc.fix.time
            print "altitude (m)", gpsc.fix.altitude
            print "eps ", gpsc.fix.eps
            print "epx ", gpsc.fix.epx
            print "epv ", gpsc.fix.epv
            print "ept ", gpsc.gpsd.fix.ept
            print "speed (m/s) ", gpsc.fix.speed
            print "climb ", gpsc.fix.climb
            print "track ", gpsc.fix.track
            print "mode ", gpsc.fix.mode
            print "sats ", gpsc.satellites
            time.sleep(0.5)

    #Error
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    #Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    finally:
        print "Stopping gps controller"
        gpsc.stopController()
        #wait for the tread to finish
        gpsc.join()

    print "Done"
