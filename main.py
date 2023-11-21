from KMLConversion import convertFileKML
from dataReader import read_in_data
from clusteringTime import labelHills
import time


def main():
	timeStart = time.perf_counter()
	data = read_in_data('data/2023_08_01__233842_gps_file.txt')
	df = labelHills(data)
	convertFileKML(df)
	endTime = time.perf_counter()
	elapsed_time = endTime - timeStart
	print(f"Time:{elapsed_time}")

if __name__ == "__main__":
	main()