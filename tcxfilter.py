#!/usr/bin/env python

import xml.etree.cElementTree as ET
import argparse
import sys
import os

argparser = argparse.ArgumentParser(description='From an origin directory containing .tcx files, copy only those files starting within a specified lat/lon box.')
argparser.add_argument('-o', '--origin', help='Origin directory containing .tcx files', required=True)
argparser.add_argument('-d', '--destination', help='Destination directory to copy files to', required=True)
argparser.add_argument('-l', '--latlon', help='Latitude/longitude boundaries of the box as lat1,lon1,lat2,lon2, ex. 39.04,-76.909,38.759,-77.49', required=True)
args = argparser.parse_args()

(lat1, lon1, lat2, lon2) = [float(f) for f in args.latlon.split(',')]
if lat1 > lat2:
    (lat1, lat2) = (lat2, lat1)
if lon1 > lon2:
    (lon1, lon2) = (lon2, lon1)
# now we have lower bounds in lat1/lon1 and upper bounds in lat2/lon2

if not os.path.isdir(args.origin):
    print("Origin directory does not exist: %s" % args.origin)
    sys.exit(1)
if not os.path.isdir(args.destination):
    os.mkdir(args.destination)

print("Starting with box (%f,%f,%f,%f), copy from %s to %s" % (lat1, lon1, lat2, lon2, args.origin, args.destination))

for file in os.listdir(args.origin):
    if file.endswith('.tcx'):
        try:
            tree = ET.parse(os.path.join(args.origin, file))
            root = tree.getroot()
            lat = float(root.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LatitudeDegrees').text)
            lon = float(root.find('.//{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LongitudeDegrees').text)
            if lat1 <= lat and lat <= lat2 and lon1 <= lon and lon <= lon2:
                print ('Copying %s' % file)
                os.system('cp %s %s' % (os.path.join(args.origin, file), args.destination))
        except AttributeError:
            # ignore files that don't have lat/lon
            pass
        except:
            print('Error parsing %s' % file)
            print(sys.exc_info()[0])


print ('Done')
