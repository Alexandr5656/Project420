import pandas
import dataReader					
import numpy as np


def findHills(df):
	flatCount = 5
	threshold = 0.25
	minHill = 5

	df['altitude'] = df['altitude'].astype(float) # Added this hear for loop to go faster

	smoothedAltitudes = []
	for i in range(len(df)):
		start = max(0, i - flatCount + 1)
		fixedAlt = sum(df['altitude'][start:i+1]) / (i - start + 1)
		smoothedAltitudes.append(fixedAlt)
	df['smoothedAltitude'] = smoothedAltitudes


	segments= []
	uphill_segment = [] # list of rows from dataframe
	currentlyUp = False
	start = None
	prev_alt = None
	for i, row in df.iterrows():
		if(i == 0):
			prev_alt = row['smoothedAltitude']
			continue  
		altitude_change = row['smoothedAltitude'] - prev_alt
		if altitude_change > threshold:
			if not currentlyUp:
				start = i - 1
				currentlyUp = True
				uphill_segment = [] # reset uphill segment
			uphill_segment.append(row)
		else:
			if currentlyUp:
				if (i - 1) - start >= minHill:
					segments.append(uphill_segment)
				currentlyUp = False
	#print(segments)
	return segments
