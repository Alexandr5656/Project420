import simplekml

def parseCoord(data):
    parts = data.split('.')
    degrees = int(parts[0]) // 100
    minutes = float(parts[0][-2:] + '.' + parts[1])
    return degrees + minutes / 60

def getCoords(line):
	coordInfo = line.split(',')
	lat = 1 if coordInfo[4] else -1
	long = 1 if coordInfo[6] else -1
	lat *= coordInfo[3]
	long *= coordInfo[5]
	return lat,long




linesAdded = 0
currentLine=0
skipCount = 20
maxLines = 25000
gpsData = "./data/2023_08_01__233842_gps_file.txt"
kml = simplekml.Kml()
lines_to_skip = 4 

with open(gpsData, 'r') as file:
    for _ in range(lines_to_skip):
        next(file) 
    for line in file:
        currentLine+=1
        if line.startswith('$GPRMC') and currentLine % skipCount == 0 and linesAdded < maxLines:
            linesAdded +=1
            data = line.split(',')
            if data[2] == 'A':
                lat,long = getCoords(line)
                kml.newpoint(coords=[(long, lat)])

kml.save("output.kml")
