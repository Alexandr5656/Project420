import simplekml
import pandas as pd

from dataReader import dataCleaner, read_in_data_pynmea
from clusteringTime import findHills

kmlTop = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"\n xmlns:gx="http://www.google.com/kml/ext/2.2">   <!-- required when using gx-prefixed elements -->\n\n<Placemark>\n  <name>gx:altitudeMode Example</name>\n  <LookAt>\n    <longitude>146.806</longitude>\n    <latitude>12.219</latitude>\n    <heading>-60</heading>\n    <tilt>70</tilt>\n    <range>6300</range>\n    <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>\n  </LookAt>\n  <LineString>\n    <extrude>1</extrude>\n    <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>\n    <coordinates>'
kmlBot = '\n    </coordinates>\n  </LineString>\n</Placemark>\n</kml>'

def parseCoord(data):
	parts = []
	try:
		parts = data.split('.')
	except:
		print(data)
	degrees = int(parts[0]) // 100
	minutes = float(parts[0][-2:] + '.' + parts[1])
	return degrees + minutes / 60

def getCoords(df):
	lat = 1 if df["lat_dir"] == "N" else -1
	long = 1 if df["lon_dir"] == "E" else -1
	lat *= parseCoord(df["lat"])
	long *= parseCoord(df["lon"])
	return lat,long


def extractAllCoords(df, indices):
	coords = []
	for i in indices:
		lat, long = getCoords(df.loc[i])
		coords.append((long, lat))
	return coords

def convertToKML(df, hills,fileName):
	kml = simplekml.Kml()

	uphillStyle = simplekml.Style()
	uphillStyle.linestyle.color = simplekml.Color.red
	uphillStyle.linestyle.width = 4
	downhillStyle = simplekml.Style()
	downhillStyle.linestyle.color = simplekml.Color.green
	downhillStyle.linestyle.width = 4


	for hill in hills:
		segment_coords = extractAllCoords(df, range(hill[0], hill[1] + 1))
		ls = kml.newlinestring(coords=segment_coords)
		ls.style = uphillStyle

	last = 0
	for hill in hills:
		start, end = hill
		if start > last:
			segment_coords = extractAllCoords(df, range(last, start))
			ls = kml.newlinestring(coords=segment_coords)
			ls.style = downhillStyle
		last = end + 1

	if last < len(df):
		segment_coords = extractAllCoords(df, range(last, len(df)))
		ls = kml.newlinestring(coords=segment_coords)
		ls.style = downhillStyle

	kml.save("outputs/"+fileName.strip(".txt")+".kml")



# if __name__ == "__main__":
#     filename = 'data/2023_08_01__233842_gps_file.txt'
#     df = read_in_data_pynmea(filename)
#     df = dataCleaner(df)
#     hills = findHills(df)
#     convertToKML(df, hills, filename)
