import os, pty, serial
from nmea import get_nmea
import pynmea2

class NavigationSystem:
    def __init__(self):
        self.master, self.slave = pty.openpty()
        self.s_name = os.ttyname(self.slave)
        self.serial = serial.Serial(self.s_name)

    def get_gps(self):
        nmea_str = get_nmea()
        self.serial.write(str.encode(nmea_str))
        line = os.read(self.master,1000).decode('utf-8')
        coordinates = pynmea2.parse(line)
        lon = round(float(coordinates.lon)/100, 6)
        lat = round(float(coordinates.lat)/100, 6)
        return lat, lon

if __name__ == "__main__":
    navigation_system = NavigationSystem()
    print(navigation_system.get_gps())