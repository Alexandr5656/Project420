import pandas
import dataReader

def findHills(df):
	threshold = .05
	HILLMIN = 50
	FLATMAX = 30
	uphillBattle = []
	i = 0
	while i < len(df):
		print(i)
		if i%20 >0:
			i+=1
			continue
		currentHill = []
		flatCount = 0
		for j in range(i+1,len(df)-1):
			lowerPoint = float(df.loc[i,'altitude'])
			higherPoint = float(df.loc[j,'altitude'])
			adjustedThreshold = threshold*len(currentHill)
			#print(higherPoint-lowerPoint)
			if (higherPoint-lowerPoint > adjustedThreshold):
				currentHill.append(higherPoint)
				flatCount=0
				#print(f"{i}   |||   Yes")
				continue
			if (higherPoint-lowerPoint < adjustedThreshold and flatCount < FLATMAX):
				flatCount+= 1
				continue
			if (higherPoint-lowerPoint < adjustedThreshold and flatCount == FLATMAX):
				if len(currentHill) > HILLMIN:
					i = j+1
					print("Hill FOund")
					uphillBattle.append(currentHill)
					break
		i+=1
	return uphillBattle
					


			






def labelHills(df):
	hillList = findHills(df)
	print(f"Hills: {len(hillList)}")
	for hill in hillList:
		for entry in hill:
			print("Found Hill")
			df[entry]["isUpHill"] = True
	return df



#if __name__ == "__main__":
#	main()