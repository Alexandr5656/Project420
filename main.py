from KMLConversion import convertToKML
from dataReader import read_in_data_pynmea, dataCleaner
from clusteringTime import findHills
import time
import os 
import pandas as pd
# Reads all files in file name to create one dataset or iterate through all gps
def readFilenamesInFolder(folder_path):
	try:
		files_and_dirs = os.listdir(folder_path)
		files = [f for f in files_and_dirs if os.path.isfile(os.path.join(folder_path, f))]
		return files
	except FileNotFoundError:
		print(f"Folder not found: {folder_path}")
		return []

# Loads data from files then converts it to a kml single files usage
def createKML(fileName):

	data = read_in_data_pynmea("data/"+fileName)
	data = dataCleaner(data)
	up = findHills(data)#[:50000])
	convertToKML(data,up,fileName)



def main():
	folder_path = 'data'
	file_names = readFilenamesInFolder(folder_path)
	dataList = []
	results = None
	for file_name in file_names:
		try:
			data = read_in_data_pynmea("data/"+file_name)
			#data = dataCleaner(data)
			dataList.append(data)
			
			print(f"Done with {file_name} and {type(data)}")
		except:
			print(file_name)
	print("Time to concat")
	results = pd.concat(dataList)
	print(type(results))
	print("Alex")
	results.to_csv('dataStoring.csv', index=False)
	#up = findHills(results)#[:50000])
	##convertToKML(data,up,"BIGDADDy.txt")


if __name__ == "__main__":
	#main()
	df = pd.read_csv('dataStoring.csv')
	print(type(df))
	data = dataCleaner(df)
	print(type(data))
	up = findHills(data)#[:50000])
	convertToKML(data,up,"tester.txt")