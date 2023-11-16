import pandas as pd

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
    print(len(UTC))
    
    data = {
        'UTC': UTC,
        'latitude': latitude,
        'latitude_dir': latitude_direction,
        'longitude': longitude,
        'longitude_dir': longitude_direction,
        'altitude': altitude,
        # 'speed': speeds
    }
    
    return pd.DataFrame(data=data)
        


if __name__ == "__main__":
    df = read_in_data('data/2023_09_28__164353_gps_file.txt')
    print(df.head())