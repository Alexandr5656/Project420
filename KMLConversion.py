import simplekml
from dataReader import read_in_data_pynmea, dataCleaner


kmlTop = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"\n xmlns:gx="http://www.google.com/kml/ext/2.2">   <!-- required when using gx-prefixed elements -->\n\n<Placemark>\n  <name>gx:altitudeMode Example</name>\n  <LookAt>\n    <longitude>146.806</longitude>\n    <latitude>12.219</latitude>\n    <heading>-60</heading>\n    <tilt>70</tilt>\n    <range>6300</range>\n    <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>\n  </LookAt>\n  <LineString>\n    <extrude>1</extrude>\n    <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>\n    <coordinates>'
kmlBot = '\n    </coordinates>\n  </LineString>\n</Placemark>\n</kml>'
def parseCoord(data):
    parts = data.split('.')
    degrees = int(parts[0]) // 100
    minutes = float(parts[0][-2:] + '.' + parts[1])
    return degrees + minutes / 60

def getCoords(df):
	lat = 1 if df["lat_dir"] == "N" else -1
	long = 1 if df["lon_dir"] == "E" else -1
	lat *= parseCoord(df["lat"])
	long *= parseCoord(df["lon"])
	return lat,long

def convertFileKML(df):
    #df = dataReader.read_in_data(file)

    linesAdded = 0
    currentLine=0
    skipCount = 40
    maxLines = 3000000
    print("asdas")
    kml = simplekml.Kml()
    multipnt = kml.newmultigeometry(name="MultiPoint")
    multipnt.style.labelstyle.scale = 0  # Remove the labels from all the points
    multipnt.style.iconstyle.color = simplekml.Color.red  
    coordString = ""  
    for index, row in df.iterrows():
        currentLine += 1
        if currentLine % skipCount == 0 and linesAdded < maxLines:
            linesAdded += 1
            lat, long = getCoords(row)
            coordString += f"{long},{lat},50\n"
            # multipnt.newpoint(coords=[(long, lat)])
    #print(coordString)
    total = kmlTop + coordString + kmlBot
    f = open("demofile3.kml", "w")
    f.write(total)
    f.close()
        #kml.save("output.kml")
if __name__ == "__main__":
     df = read_in_data_pynmea('data/2023_08_01__233842_gps_file.txt')
     df = dataCleaner(df)
     convertFileKML(df)
