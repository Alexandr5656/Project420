import pandas
import dataReader

def main():
	df = dataReader.read_in_data("data/2023_09_28__164353_gps_file.txt")
	df

if __name__ == "__main__":
	main()