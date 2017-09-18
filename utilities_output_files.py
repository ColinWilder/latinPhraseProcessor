# These are utilities for archiving data and output files.
# They can be used to read data files and to write new data files.
# They make use of a simple index file which tells the calling program what the current data folder number is. 

# gibs me dat
import os, datetime

def newOutputBasePath():
    # set basePath for output
    cwd=os.getcwd() # when you run the program the cwd reverts back to the default
    # print("cwd: \t\t" + cwd) # assumes you are running these utilities in same place as main program
    outputDir="ctp_output" # the CTP prefix is special to the Catalog Title Processor project
    basePath=os.path.join(cwd,outputDir)
    # print("basePath: \t" + basePath)
    return basePath

def currentIndex():
    # set specific path of index file
    indexPath= newOutputBasePath() +'/index.txt'
    print("indexPath: \t\t" + indexPath)
    
    # find the index of the most recent output
    currentIndex=findCurrentOutputIndex(indexPath) # see findCurrentOutputIndex function below
    print("currentIndex: \t\t" + str(currentIndex))
    
    # increment index for next time and write it to the index file for next time
    currentIndex+=1
    f = open(indexPath, "w")
    f.write(str(currentIndex)) # print to output
    f.close
    
    return currentIndex-1

def makeNewOutputFolder(currentIndex, newOutputBasePath):
	newFolderName="ctp_output"+str(currentIndex)
	outputFolderPath=newOutputBasePath+'/'+newFolderName
	if not os.path.exists(outputFolderPath):
		os.makedirs(outputFolderPath)
	return outputFolderPath
        
    
def findCurrentOutputIndex(indexPath): # returns the index of the current output folder based on the index file
    #read and increment the index file
    f = open(indexPath, "r")
    currentIndex =  int(f.readline())
    f.close()
    return currentIndex # should return an integer = current output index
    
