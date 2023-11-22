from datetime import datetime
from matplotlib import pyplot as plt
import pandas as pd
import pynmea2
from geopy.distance import distance
import numpy as np


# method being used, uses pynmea
def read_in_data_pynmea(filename):
    GPS_lines = []
    file = open(filename, "r")
    lines = file.readlines() # get file lines
    # loop through lines
    for line in lines:
        # skip initial file lines
        if(line[0] != "$"):
            continue
        try:
            # only care about GPGGA data
            if line.startswith("$GPGGA"):
                msg = pynmea2.parse(line)
                # convert timestamp to string
                msg.timestamp = msg.timestamp.strftime("%H:%M:%S:%f")
                # only need GGA because we don't need speed necessarily from RMC
                if(msg.sentence_type == "GGA"):
                    GPS_lines.append(msg) # only append the array of data
        # if error ignore and continue
        except pynmea2.ParseError as e:
            continue
    # get column names for dataframe
    column_names = []
    for field in GPS_lines[0].fields:
        column_names.append(field[1])
    # make dataframe with only grabbing data array from GPS_lines, with the column_names
    return pd.DataFrame(data=[row.data for row in GPS_lines], columns=column_names)

# clean the data
def dataCleaner(dataframe: pd.DataFrame):
    
    rows_to_drop = set() # stores the rows we will delete from dataframe
    diff_between_points = [] # for testing 
    speed_arr = [] # for testing
    # loop through all rows in dataframe
    for index, row in dataframe.iterrows():
        if index == 0:
            prev = row
            continue
        else:
            # delete if data is not quality of 1 or 2
            if(row.gps_qual != '1' and row.gps_qual != '2' ):
                rows_to_drop.add(index)
                continue
            
            # convert latitude and longitude to degree format
            lat_row = pynmea2.dm_to_sd(row['lat'])
            lat_prev = pynmea2.dm_to_sd(prev['lat'])
            lon_row = pynmea2.dm_to_sd(row['lon'])
            lon_prev = pynmea2.dm_to_sd(prev['lon'])
            
            # get distance
            distance_2d, distance_3d = get_distance(lat_row, lat_prev, lon_row, lon_prev, float(row.altitude), float(prev.altitude))
            # get time diff
            time_diff = convert_to_datetime(row.timestamp) - convert_to_datetime(prev.timestamp)
            # get speed
            speed = get_speed(distance_3d, time_diff.microseconds)
            
            # if speed < 0.5 m/s delete
            if speed < .5:
                rows_to_drop.add(index)
            
            # remove some stopping data points where not moving, removed so not as precise
            # if(distance_2d < 0.1):
            #     rows_to_drop.add(index)
            
            # set previous
            prev = row

    # print('data length '+ str(len(dataframe)))
    
    # delete points from dataframe
    dataframe = dataframe.drop(index=rows_to_drop)
    # reset so no skips in indexes
    dataframe.reset_index(drop=True, inplace=True)
    # print('cleaned data length '+str(len(dataframe)))
    
    return dataframe

# get distance, 2D and 3D
def get_distance(lat_row, lat_prev, lon_row, lon_prev, alt_row, alt_prev):
    distance_2d = distance((lat_row, lon_row), (lat_prev, lon_prev)).m
    distance_3d = np.sqrt(distance_2d**2 +(alt_row-alt_prev)**2)
    return (distance_2d, distance_3d)

# convert date string from pynmea to datetime object
def convert_to_datetime(time_string):
    return datetime.strptime(time_string, "%H:%M:%S:%f")

# distance is meters, time is microseconds
def get_speed(distance, time):
    if time == 0:
        return 0
    # check for divide by zero errors
    try:
        speed = (distance/time)*1000000 # convert to m/s
        return speed
    except RuntimeError as  e:
        return 0

# if __name__ == "__main__":
# #    df = read_in_data('data/2023_09_28__164353_gps_file.txt')
#    df = read_in_data_pynmea('Test-Suites/8_14_1000_lines.txt')
#    dataCleaner(df)
#    print(df.head())