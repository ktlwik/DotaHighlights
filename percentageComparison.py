ocvrFile = ["VPvsLiquid(ocvr).txt", "EGvsVP(ocvr).txt", "NaviVSEG(ocvr).txt"]
firstAlgo = ["VPvsLiquid(1stalgo).txt", "EGvsVP(2ndalgo).txt", "NaviVsEG(1stalgo).txt"]
secondAlgo = ["VPvsLiquid(2ndalgo).txt","EGvsVP(1stalgo).txt", "NaviVsEG(2ndalgo).txt"]

def secs(str):
	x, y = str.split(":")
	return int(x) * 60 + int(y)

for i in range(len(ocvrFile)):
	with open(ocvrFile[i]) as f:
		best = f.readlines()
	with open(firstAlgo[i]) as d:
		content1 = d.readlines()
	with open(secondAlgo[i]) as e:
		content2 = e.readlines()
	range1 = [0] * 5000
	range2 = [0] * 5000
	bestLength = 0
	content1Length = 0
	content2Length = 0
	data = []
	#print (i)
	for line in best:
		#print line
		x,y = line.split("-")
		z,w = secs(x), secs(y)
		bestLength += w-z + 1
		data.append([z, w + 1])
	for x, y in data:
		for j in range(x, y):
			range1[j] = range2[j] = 1
	data = []
	for line in content1:
		x,y = line.split(" ")
		data.append([int(x), int(y) + 1])
	
	for x, y in data:
#		print (x, y, y-x)
		content1Length += y - x 
		for j in range(x, y):
			range1[j] = range1[j] + 1
    
	data = []
	for line in content2:
		x,y = line.split(" ")
		data.append([int(x), int(y) + 1])
	for x, y in data:
		content2Length += y-x
		for j in range(x, y):
			range2[j] = range2[j] + 1
   	r1count = 0
   	r2count = 0
   	for t in range(4999):
   		if (range1[t] == 2):
   			r1count = r1count + 1
		if (range2[t] == 2):
			r2count = r2count + 1

#	print (bestLength, content1Length, content2Length)
#	print (r1count, r2count)
	print (100-r1count*100/min(bestLength, content1Length), 100-r2count*100/min(bestLength, content2Length))

