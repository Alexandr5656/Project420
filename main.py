from KMLConversion import convertToKML
from dataReader import read_in_data
from clusteringTime import findHills
import time
import os 
def read_filenames_in_folder(folder_path):
	try:
		files_and_dirs = os.listdir(folder_path)
		files = [f for f in files_and_dirs if os.path.isfile(os.path.join(folder_path, f))]
		return files
	except FileNotFoundError:
		print(f"Folder not found: {folder_path}")
		return []


def createKML(fileName):

	data = read_in_data("data/"+fileName)
	up = findHills(data)#[:50000])
	convertToKML(data,up,fileName)

def main():
	folder_path = 'data'
	file_names = read_filenames_in_folder(folder_path)
	for file_name in file_names:
		try:
			createKML(file_name)
		except:
			print(file_name)

if __name__ == "__main__":
	main()