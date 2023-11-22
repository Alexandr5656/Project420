from KMLConversion import convertToKML
from dataReader import read_in_data_pynmea, dataCleaner
from clusteringTime import findHills
import os
import pandas as pd
import simplekml

# Reads in all files in a folder
def readFilenamesInFolder(folder_path):
	try:
		files_and_dirs = os.listdir(folder_path)
		files = [f for f in files_and_dirs if os.path.isfile(os.path.join(folder_path, f))]
		return files
	except FileNotFoundError:
		print(f"Folder not found: {folder_path}")
		return []




#Loads in data then converts to kml
def singleSet(fileName):
	kml = simplekml.Kml()
	fPath = 'data'
	data = read_in_data_pynmea(os.path.join(fPath, fileName))
	data = dataCleaner(data)
	up = findHills(data)
	convertToKML(data, up, kml)
	kml.save(f'{fileName[:-4]}.kml')

#Loads in all data then converts to kml
def fullDataSet():
	kml = simplekml.Kml()
	filePart = 1
	fPath = 'data'
	fileNames = readFilenamesInFolder(fPath)

	for fileName in fileNames:
		print(f"Starting {fileName}")
		data = read_in_data_pynmea(os.path.join(fPath, fileName))
		data = dataCleaner(data)
		up = findHills(data)
		convertToKML(data, up, kml)

		kml_string = kml.kml()
		estimated_size = len(kml_string.encode('utf-8'))
		if estimated_size > 4.5 * 1024 * 1024:
			kml.save(f'combinedPart{filePart}.kml')
			print(f"File saved: combinedPart{filePart}.kml")
			filePart += 1
			kml = simplekml.Kml()
			convertToKML(data, up, kml)
		print(f"Ending {fileName}")


	if estimated_size > 0:
		kml.save(f'combinedPart{filePart}.kml')
		print(f"File saved: combinedPart{filePart}.kml")


if __name__ == "__main__":
	fullDataSet() # This is for the full data set and works only if data is in data folder
	#singleSet("2023_08_01__233842_gps_file.txt") # This assumes the data is in the data folder