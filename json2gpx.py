"""
json2gps.py
"""

import argparse
import datetime
import json
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser()
parser.add_argument('file_in')
parser.add_argument('file_out')
args = parser.parse_args()

with open(args.file_in) as filein:
  data = json.load(filein)
  print("%s loaded" % args.file_in)

try:
    # create the file structure
    gpx_out = ET.Element('gpx')

    gpx_out.set("version", "1.1")
    gpx_out.set("creator", "https://github.com/MBunel/json2gpx")

    # Metadonnées
    metadata = ET.SubElement(gpx_out, 'metadata')
    
    name = ET.SubElement(metadata, 'name')
    name.text = data["name"]

    desc = ET.SubElement(metadata, 'desc')
    desc.text = "Automatic transformation of %s file" % data["name"]

    trk = ET.SubElement(gpx_out, 'trk')
    trkseg = ET.SubElement(trk, 'trkseg')

    for pos in data["data"]:
        trkpt = ET.SubElement(trkseg, 'trkpt')
        trkpt.set("lat", str(pos["newValue"]["position"]["lat"]))
        trkpt.set("lon", str(pos["newValue"]["position"]["lng"]))
        
        # Time stamp
        time = ET.SubElement(trkpt, 'time')
        time.text = datetime.datetime.fromtimestamp(pos["timestamp"]//1000).isoformat()


        # create a new XML file with the results
        #import pdb; pdb.set_trace()
        
        gpx_out_str = ET.tostring(gpx_out)
        
        with open(args.file_out, 'wb') as fileout:
            fileout.write(gpx_out_str) 
 
except KeyError:
    print("Error with %s" % args.file_in)
