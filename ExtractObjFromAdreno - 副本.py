import sys

# KeyList 该行含有的信息，比如含法线，顶点，UV信息
# KeyCount 该行每个信息含有的数字列数，比如每个法线含有3个数字，顶点3个数字，UV2个数字

#vertexKeyList = ["index", "normal", "vertex", "uv"]
#vertexKeyCount = [1, 3, 3, 2]

vertexKeyList = ["index", "inblendindex", "inblendweight", "normal", "vertex", "uv"]
vertexKeyCount = [1, 4, 3, 3, 3, 2]

#vertexKeyList = ["index", "vertex", "normal", "uv", "tagent"]
#vertexKeyCount = [1, 3, 3, 2, 3]

faceKeyList = ["index", "face"]
faceKeyCount = [1, 3]


vertextInfoTotalCount = 0
faceInfoTotalCount = 0
vertexPosList = list()
normalPosList = list()
uvPosList = list()
facePosList = list()
faceCount = 1

def replaceAll(filename):
	f = open(filename,'r')
	vertexList = list()
	normalList = list()
	uvList = list()
	faceIndexList = list()
	faceList = list()
	
	global faceCount
	faceCount = 1
	GetKeyPosInfo()
	
	for line in f.readlines():
		line = line.replace("	", " ").replace(",", " ").replace("  ", " ").replace("    ", " ").replace("\n", "")
		splitLine = line.split(" ")
		if len(splitLine) > 4:
			HandleVertexInfo(splitLine, vertexList, normalList, uvList)
		else:
			HandleFaceInfo(splitLine, faceIndexList, faceList)
	f.close()
	
	f = open(GetResultFileName(f.name), 'w')
	f.write("%s" % '\n'.join(vertexList))
	f.write("\n\n\n")
	f.write("%s" % '\n'.join(normalList))
	f.write("\n\n\n")
	f.write("%s" % '\n'.join(uvList))
	f.write("\n\n\n")
	f.write("%s" % '\n'.join(faceIndexList))
	f.write("\n\n\n")
	f.write("%s" % '\n'.join(faceList))
	f.close()
	
def GetKeyPosInfo():
	global vertexPosList
	global normalPosList
	global uvPosList
	global facePosList
	global vertextInfoTotalCount
	global faceInfoTotalCount
	
	curIndex = 0
	for index, key in enumerate(vertexKeyList):
		if key == "vertex":
			vertexPosList = [curIndex, curIndex+1, curIndex+2]
		elif key == "normal":
			normalPosList = [curIndex, curIndex+1, curIndex+2]
		elif key == "uv":
			uvPosList = [curIndex, curIndex+1]
		curIndex = curIndex + vertexKeyCount[index]
		vertextInfoTotalCount = vertextInfoTotalCount + vertexKeyCount[index]
		
	curIndex = 0	
	for index, key in enumerate(faceKeyList):
		if key == "face":
			facePosList = [curIndex, curIndex+1, curIndex+2]
		curIndex = curIndex + faceKeyCount[index]
		faceInfoTotalCount = faceInfoTotalCount + faceKeyCount[index]
	
def HandleVertexInfo(info, vertexList, normalList, uvList):
	global vertexPosList
	global normalPosList
	global uvPosList
	global vertextInfoTotalCount
	
	if len(info) >= vertextInfoTotalCount:
		vertexInfo = "v" + " " + info[vertexPosList[0]] + " " + info[vertexPosList[1]] + " " + info[vertexPosList[2]]
		normalInfo = "vn" + " " + info[normalPosList[0]] + " " + info[normalPosList[1]] + " " + info[normalPosList[2]]
		uvInfo = "vt" + " " + info[uvPosList[0]] + " " + info[uvPosList[1]]
		vertexList.append(vertexInfo)
		normalList.append(normalInfo)
		uvList.append(uvInfo)
	
def HandleFaceInfo(info, faceIndexList, faceList):
	global facePosList
	global faceInfoTotalCount
	global faceCount
	
	if len(info) >= faceInfoTotalCount:
		index1 = str(int(info[facePosList[0]])+1)
		index2 = str(int(info[facePosList[1]])+1)
		index3 = str(int(info[facePosList[2]])+1)
		index1 = index1 + "/" + index1 + "/" + index1
		index2 = index2 + "/" + index2 + "/" + index2
		index3 = index3 + "/" + index3 + "/" + index3
		
		#有时候给出的顶点顺序是相反的，导致面反掉了，要试一下哪种是对的
		faceInfo = "f" + " " + index3 + " " + index2 + " " + index1
		#faceInfo = "f" + " " + index1 + " " + index2 + " " + index3
		
		faceList.append(faceInfo)
		
		strCount = str(faceCount)
		faceIndexInfo = "f" + " " + strCount + "/" + strCount + "/" + strCount
		faceIndexList.append(faceIndexInfo)
		faceCount = faceCount + 1
		
def GetResultFileName(rawFileName):
	splitName = rawFileName.split('.')
	splitName[-1] = ''
	resultFileName = ''.join(splitName) + ".obj"
	return resultFileName
	
	
if __name__ == '__main__':
	if len(sys.argv) == 1:
		print("Please provide filename")
	else:
		files = sys.argv[1:]
		for x in files:
			replaceAll(x)
			
			