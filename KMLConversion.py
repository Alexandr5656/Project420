import simplekml
import dataReader
def parseCoord(data):
    parts = data.split('.')
    degrees = int(parts[0]) // 100
    minutes = float(parts[0][-2:] + '.' + parts[1])
    return degrees + minutes / 60

def getCoords(df):
	lat = 1 if df["latitude_dir"] == "N" else -1
	long = 1 if df["longitude_dir"] == "E" else -1
	lat *= parseCoord(df["latitude"])
	long *= parseCoord(df["longitude"])
	return lat,long

def convertFileKML(file):
    df = dataReader.read_in_data(file)

    linesAdded = 0
    currentLine=0
    skipCount = 40
    maxLines = 3000000

    kml = simplekml.Kml()
    for index, row in df.iterrows():
        currentLine += 1
        if currentLine % skipCount == 0 and linesAdded < maxLines:
            linesAdded += 1
            lat, long = getCoords(row)
            kml.newpoint(coords=[(long, lat)])

    kml.save("output.kml")
if __name__ == "__main__":
     convertFileKML('data/2023_08_02__183833_gps_file.txt')