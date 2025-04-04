#Made by Nicholas Velcea
#this script is intended to take files generated in a temp folder and sort them according to our groups directory setup.
#After running and sorting the files,
import os
import shutil
from time import sleep
import sys


tempPath = r"C:\NUCAR\primeHex\temp"
mainPath =r"C:\NUCAR\primeHex\mainDir"
#r is inserted before string to make raw string - prevents unicode escape errors
#total threads = first parameter
#thread id = 2nd parameter
totalThreads = sys.argv[1]
tid = sys.argv[2]
while(1==1):
    if(len(os.listdir(tempPath)) == 0): ## prevents from cycling through constantly if folder is empty
        sleep(.1)
    else:
        for file in os.listdir(tempPath): #iterates through all files in folder
            fileName = file.strip('.txt')
            if(int(fileName)%totalThreads == tid):
                tempFileDir = (os.path.join(tempPath, file)) #finds directory of exact file
                if(len(fileName) % 2 == 1): ##guarantees even number of digits in file name
                    fileName = "0" + fileName
                directories = []
                for x in range(0,int(len(fileName)/2)): ##separates file name into groups of two numbers
                    directories.append(fileName[2*x:2*x+2])
                filePath = mainPath
                for x in range(0,len(directories)-1):
                    filePath += str("\\")
                    filePath += directories[x]
                    if not os.path.exists(filePath):
                        os.makedirs(filePath)
                newFileDir = filePath + "\\" + directories[len(directories)-1] + ".txt";
                shutil.copyfile(tempFileDir, newFileDir);
                os.remove(tempFileDir);

