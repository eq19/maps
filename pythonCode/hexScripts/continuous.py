import hexWrapper

current = 0
color = 0
while True:
	f = open("./bigHexFile.txt","a+")
	f.write("%s" % str(color) + "\n")
	f.close()
	color = hexWrapper.runHex(str(current),str(color),str(current+10**11),0,False)
	current = current+10**11
