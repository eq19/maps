##Made by Nicholas Velcea
#this program is intended to take unshifted files from the HexSieve progam, and shift them so that they are consistant
#with previous files.
#NOTE:::: Once this is implelemented on the NUCAR Server, oldPath, slashVar, and newPath must be changed. Their values
#for the server system are currently commented out near the top of the script.
#Also the program might need to be adjusted for whatever 00000 buffering occurs from HexSieve, and whatever is desiered.

import os
import shutil
from time import sleep
import sys
import getpass

username = getpass.getuser()

oldPath = "/temp2"
#oldPath = r"C:\NUCAR\primeHex\temp"
#slashVar = oldPath[2]
slashVar = "/"
newPath = "/temp"
#newPath = r"C:\NUCAR\primeHex\tempSorted"

fileNum = sys.argv[1]
shift = int(sys.argv[2])

while(fileNum==0): #there is a separate loop for the first file because you do not need to shift it
    #also is while loop so that it will repeat if correct file is not yet present
    for file in os.listdir(oldPath):
        thisFile = file.strip('.txt')
        if(0==int(thisFile)):
            with open(oldPath+ slashVar + file, "r") as f: ## this gets the value of the last line in the file
                add = int(f.readlines(0)[99])
                shift=add
                print(shift)
                f.close()
            #These four lines contain the old and new file directories, copys the file over, and removes the old file
            oldFilePath = oldPath + slashVar + file
            newFilePath = newPath + slashVar + ("{:0>10d}".format(fileNum)) + ".txt"
            shutil.copy(oldFilePath,newFilePath)
            os.remove(oldFilePath)
            fileNum+=1

while(fileNum>0):
    sleep(1) #delay to not waste resources
    thisFile = ("{:0>10d}".format(fileNum)) + ".txt"
    testFilePath = oldPath + slashVar + thisFile
    if(os.path.exists(testFilePath)):
        sleep(1) #delay to not waste resources
        thisFile = thisFile.strip(".txt") ## gets the value of the current file
        print("This File is: " + thisFile) ##debug shit
        with open(testFilePath, "r") as f:
            fileList = f.readlines(0)
            for x  in range (0,101): #Makes integer list of each line in selected file & shifts each cell accordingly
                fileList[x]=int(fileList[x])
                fileList[x]=(fileList[x]+shift)%6 #shifting
            print(fileList)
            shift = fileList[100] # value of last line (shifted)
            print(shift)
            f.close()
        with open(oldPath + slashVar + file, "w") as f:
            for x in range (0,101): #rewrites the file
                f.write(str(fileList[x])+'\n')
            f.close()
        #this deletes the old file, and writes a new file
        oldFilePath = oldPath + slashVar + file
        newFilePath = newPath + slashVar + ("{:0>10d}".format(fileNum)) + ".txt"
        shutil.copy(oldFilePath, newFilePath)
        os.remove(oldFilePath)
        fileNum+=1


