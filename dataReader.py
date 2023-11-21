from matplotlib import pyplot as plt
import pandas as pd
import pynmea2

def read_in_data(filename):
    GPGGA_lines = [] # has altitude
    GPRMC_lines = [] # has speed
    file = open(filename, "r")
    lines = file.readlines()
    for index, line in enumerate(lines):
        # skip initial file lines
        if(line[0] != "$"):
            continue
        # TODO remove if invalid V (might not have to worry about)
        split_data = line.strip('\n').split(',') # split by comma delimiter, and take out new line
        if(index >= 6):
            if(float(split_data[1]) - float(lines[index-1].split(',')[1]) != 0.250):
                continue
        if(split_data[0] == "$GPGGA"):
            GPGGA_lines.append(split_data)
        elif(split_data[0] == "$GPRMC"):
            # if invalid as denoted by 'V' then skip
            if(split_data[3] ==  'V'):
                continue_again = True
                continue
            GPRMC_lines.append(split_data)
            
    # speeds = [row[7] for row in GPRMC_lines] # get only the speed column from GPRMC line
    UTC = [row[1] for row in GPGGA_lines]
    latitude = [row[2] for row in GPGGA_lines]
    latitude_direction = [row[3] for row in GPGGA_lines]
    longitude = [row[4] for row in GPGGA_lines]
    longitude_direction = [row[5] for row in GPGGA_lines]
    altitude = [row[9] for row in GPGGA_lines]
    
    # print(len(speeds))
    # print(len(UTC))
    
    data = {
        'UTC': UTC,
        'latitude': latitude,
        'latitude_dir': latitude_direction,
        'longitude': longitude,
        'longitude_dir': longitude_direction,
        'altitude': altitude,
        'isUpHill' : False
        # 'speed': speeds
    }
    
    return pd.DataFrame(data=data)

def read_in_data_pynmea(filename):
    GPS_lines = []
    file = open(filename, "r")
    lines = file.readlines()
    for line in lines:
        # skip initial file lines
        if(line[0] != "$"):
            continue
        try:
            msg = pynmea2.parse(line)
            # only need GGA because we don't need speed necessarily from RMC
            if(msg.sentence_type == "GGA"):
                GPS_lines.append(msg) # only append the array of data
        # if error ignore and continue
        except pynmea2.ParseError as e:
            continue
    # get column names
    column_names = []
    for field in GPS_lines[0].fields:
        column_names.append(field[1])
    # make dataframe with only grabbing data array from GPS_lines, with the column_names
    return pd.DataFrame(data=[row.data for row in GPS_lines], columns=column_names)

def dataCleaner(dataframe: pd.DataFrame):
    # remove multiple data points same location
    rows_to_drop = []
    diff_between_points = []
    for index, row in dataframe.iterrows():
        if index == 0:
            prev = row
            continue
        else:
            diff = abs(float(prev['lat']) - float(row['lat']))
            diff_between_points.append(diff)
            if(diff >= 2.5):
                rows_to_drop.append(index)
            if(prev['lat'] == row['lat'] and prev['lon'] == row['lon']):
                rows_to_drop.append(index)
    diff_between_points.sort(reverse=True)
    
    dataframe = dataframe.drop(index=rows_to_drop)
    # plt.hist(diff_between_points)
    # plt.show()
    return dataframe
        


if __name__ == "__main__":
#    df = read_in_data('data/2023_09_28__164353_gps_file.txt')
   df = read_in_data_pynmea('data/2023_09_28__164353_gps_file.txt')
   dataCleaner(df)
#    print(df.head())