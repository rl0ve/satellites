import numpy as np
import ephem
import datetime
import os
import pycurl
import json
import jsonify

ELEVATION_BASE_URL = 'https://maps.googleapis.com/maps/api/elevation/json'

#os.chdir(".")
# Google Elevation API info
myKey = "AIzaSyAZgMQ6edjbiq3hO5Aq2XhWO5bo0Ot2nfE"

# Downloads current NORAD Two-Line Element Sets for GPS
def downloadTLE():
    with open('./files/NORAD_TLE_GPS.txt', 'wb') as f:
        c = pycurl.Curl()
        c.setopt(c.URL, 'http://celestrak.com/NORAD/elements/gps-ops.txt')
        c.setopt(c.WRITEDATA, f)
        c.perform()
        c.close()

# Loads a TLE file and creates a list of satellites
def loadTLE(filename):
    f = open(filename)
    satlist = []
    l1 = f.readline()
    while l1:
        l2 = f.readline()
        l3 = f.readline()
        sat = ephem.readtle(l1,l2,l3)
        satlist.append(sat)
        #print sat.name
        l1 = f.readline()

    f.close()
    print "%i satellites loaded"%len(satlist)
    return satlist


def getVisibleGPSSatellites(lat, lon):
    filename = './files/NORAD_TLE_GPS.txt'
    sat      = loadTLE(filename)
    nSat     = len(sat)

    rx      = ephem.Observer()
    rx.lat  = np.deg2rad(lat)
    rx.long = np.deg2rad(lon)

    # Compute satellite locations at time = now and count visible satellites
    sat_alt, sat_az, sat_vis = [], [], []
    vs = 0
    date_time = datetime.datetime.now()

    rx.date = date_time
    for i in range(0, nSat):
        biif1 = sat[i]
        biif1.compute(rx)
        sat_alt.append(np.rad2deg(biif1.alt))
        sat_az.append( np.rad2deg(biif1.az ))
        if np.rad2deg(biif1.alt) > 15:
            vs = vs + 1
            sat_vis.append(1)
        else:
            sat_vis.append(0)

    by_satellite = ([{"sat_alt": altitude, "sat_az": azimuth, "sat_vis": visibility}
                            for altitude, azimuth, visibility in zip(sat_alt, sat_az, sat_vis)])

    number_visible = sat_vis.count(1)

    print (str(number_visible) + "are visible")
    print by_satellite
    # print ({'sat_alt': sat_alt, 'sat_az': sat_az, 'sat_vis': sat_vis})
    # return {'sat_alt': sat_alt, 'sat_az': sat_az, 'sat_vis': sat_vis}

    return number_visible, by_satellite
# downloadTLE()
# getVisibleGPSSatellites(42.35, -71.0)
