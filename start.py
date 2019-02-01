# import for the console colors
from consoleColors import bcolors
from customExceptions import coreFileNotFoundException
from fileLoader import fileLoad
import os
import time
import json

# this is the data loader class
# Please note that we are requiring specific input of files
# Host ID (space) Host Name
class classDataLoad:
    
    # this is the default constructor
    # this also takes an optional parameter of the data file location
    
    # data file names
    strDataFileLocation = None
    strDataTrainingLabels = None
    strDataTestLabels = None
    strHostGraphRaw = None
    
    # all the meta data for all the files
    metaDataHostNames = None
    metaDataTrainLabels = None
    metaDataTestLabels = None
    metaDataHostGraph = None
    
    def __init__(self, paramDataFileLocation = None, paramTrainFileLabelLocation = None, paramTestFileLabelLocation = None, paramHostGraphRaw = None):
        print('Initializing constructor for data load class')
        try:
            self.strDataFileLocation = paramDataFileLocation
            self.strDataTrainingLabels = paramTrainFileLabelLocation
            self.strDataTestLabels = paramTestFileLabelLocation
            self.strHostGraphRaw = paramHostGraphRaw
            self.fnCheckFile()
            self.fnLoadFilesToDisk()
        except coreFileNotFoundException as cfnfe:
            print(bcolors.FAIL + 'Core file not found, core file name : [' + cfnfe.message + '], please check if all the core files exists at the root folder. \nERR 101: Program FAIL! The program will now exit')
        
    def fnCheckFile(self):
        try:
            # check if the given file already exist or not ?
            # boolean default the user input value
            boolContinueWithDefaultLocation = False
            
            # check all the core file paths
            print('Checking core files')
            self.fnCheckFilePath(self.strDataFileLocation)
            self.fnCheckFilePath(self.strDataTrainingLabels)
            self.fnCheckFilePath(self.strHostGraphRaw)
            self.fnCheckFilePath(self.strDataTestLabels)
            
        except coreFileNotFoundException as cfnfe:
            raise coreFileNotFoundException(cfnfe.message)
             
    def fnLoadFilesToDisk(self):
        # now we have the files, we need to load the files to the disk
        timeStart = time.time()
        self.metaDataHostNames = fileLoad(self.strDataFileLocation).fnLoadHostNames()
        self.metaDataHostGraph = fileLoad(self.strHostGraphRaw).fnLoadHostGraph(self.metaDataHostNames)
        self.metaDataHostGraph = fileLoad(self.strDataTrainingLabels).fnInjectTrainLabelsToHostGraph(self.metaDataHostGraph, self.metaDataHostNames)
        print (json.dumps(self.metaDataHostGraph, indent=4, cls=CustomEncoder))
        listPredictedTestLabels = fileLoad(self.metaDataHostGraph).fnPredictTestLabels(self.strDataTestLabels, self.metaDataHostNames)
        timeEnd = time.time()
        print('Time taken : ' + str(round(timeEnd - timeStart,2)) + ' seconds ')
        return None
          
    def fnCheckFilePath(self, paramStrFileLocation):
        strFilePath = os.getcwd() + '/' + paramStrFileLocation
        if(os.path.isfile(strFilePath)):
            print('Checking file at path '+  str(strFilePath) + bcolors.OKGREEN + ' File exists' + bcolors.ENDC)
            return True
        
        # if you have reached here then it means that file is not found
        # throw the exception
        raise coreFileNotFoundException(paramStrFileLocation)
                
class CustomEncoder(json.JSONEncoder):
      def default(self, o):
          if isinstance(o, datetime):
              return {'__datetime__': o.replace(microsecond=0).isoformat()}
          return {'__{}__'.format(o.__class__.__name__): o.__dict__}
         
classDataLoadObj = classDataLoad(
    paramDataFileLocation = 'new_hostnames.csv',
    paramTrainFileLabelLocation = 'webspam-uk2006-set1-labels-DomainOrTwoHumans.txt',
    paramHostGraphRaw = 'uk-2006-05.hostgraph_weighted.txt',
    paramTestFileLabelLocation = 'webspam-uk2006-set2-labels-DomainOrTwoHumans.txt'
    )
