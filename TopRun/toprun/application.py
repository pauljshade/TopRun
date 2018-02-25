'''
Created on 11 Feb 2018

@author: paulj
'''
import json
import os

from toprun.fileProcessor import fitnessFile
from toprun.dataProcessors import runHeader

class config(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''        
        self.__config=self.__readConfig()
        
        return
    
    def __readConfig(self):
        
        with open('../config/config.json') as json_data_file:
            data = json.load(json_data_file)
        
        return data

    def getUser(self):
        return self.__config['appConfig']['defaultUser']

    def getApplicationDataDir(self):
        return self.__config['appConfig']['applicationDataDir']
    
    def getTitleFormat(self):
        return self.__config['appConfig']['defaultTitle']
    
    def getProcessDir(self):
        
        processor=self.__config['appConfig']['defaultProcessDir']
        
        if '%APP_DIR%' in processor :
            processor=processor.replace('%APP_DIR%',self.getApplicationDataDir())
        
        return processor
    
class application(object):
    
    def __init__(self):
        
        self.__config=config()
        self.__menu=menu(self)
        
        return
    
    def getConfig(self):
        return self.__config
    
    def getMenu(self):
        return self.__menu
    
class menu(object):
    
    def __init__(self, application):
        
        self.__application=application
        self.__fileList=[]
        
        return
    
    def showMainMenu(self):
        
        # test input options
        print(u"****************************************************************************************************")
        print(u"****************************************************************************************************")
        print(u"**                                                                                                  ")
        print(u"** Input options :                                                                                  ")
        print(u"**   Configuration                                                                                                ")
        print(u"**     *01*. Change user name (paul.j.shade@gmail.com)                                                 ")
        print(u"**     *02*. Change application directory (C:/Users/paulj/Google Drive/ApplicationData/toprun)         ")
        print(u"**     *03*. Change input directory       (%APP_DIR%/toprocess/)                                       ")
        print(u"**                                                                                                   ")
        print(u"**   Load data                                                    ")
        print(u"**     *04*. Look for new files                                    ")
        print(u"**                                                                                                  ")
        print(u"**    99. Exit                                                                                      ")
        print(u"**                                                                                                  ")
        print(u"****************************************************************************************************")
        print(u"****************************************************************************************************")
        print("\n")
        self.executeSelection(input("Select Option > "))
        
    def showLoadMenu(self):
        
        proDir=self.__application.getConfig().getProcessDir()
        fileList=os.listdir(proDir)
        self.__fileList=fileList
        
        # test input options
        print(u"****************************************************************************************************")
        print(u"****************************************************************************************************")
        print(u"**                                                                                                  ")
        print(u"** Files Present :                                                                                  ")
        for i in range(0,len(fileList)) :
            theRawRunFile=fitnessFile(proDir+'\\'+fileList[i])
            theRawRunFile.retrieveRawMessages()
            theRunHeader=runHeader(theRawRunFile,self.__application.getConfig().getUser()).getHeader()

            print("**    %s. %s %s %04.1fkm %s %s" % (str(7001+i), fileList[i], theRunHeader['startTime'],theRunHeader['totalMetres']/1000, theRunHeader['activity'], theRunHeader['GPSFlag']))

        print(u"**                                                                                                  ")
        print(u"**    9999. Back to main menu                                                                                      ")
        print(u"**                                                                                                  ")
        print(u"****************************************************************************************************")
        print(u"****************************************************************************************************")
        print("\n")
        self.executeSelection(input("Select Option > "))    

    def executeSelection(self,menuChoice):
        
        if menuChoice=="99" :
            self.__selectExit()
        if menuChoice=="04" :
            self.__selectLoad()
        if len(menuChoice)==4 and menuChoice[:1]=="7" :
            self.__selectFile(menuChoice)            
        return
    
    
    
    def __selectExit(self):
        
        print(u"\n****************************************************************************************************")
        print("                                       Exiting ... bye!")
        print(u"****************************************************************************************************")
        print("\n")
        quit()        
            
    def __selectLoad(self):
        
        print(u"\n****************************************************************************************************")
        print("                                       Load data")
        print(u"****************************************************************************************************")
        print("\n")
        self.showLoadMenu()       
            
    def __selectFile(self,choice):
        
        print(u"\n****************************************************************************************************")
        print("                                       Validate the File")
        print(u"****************************************************************************************************")
        print("\n")
        
        proDir=self.__application.getConfig().getProcessDir()
        file=self.__fileList[int(choice)-7001]
        theRawRunFile=fitnessFile(proDir+'//'+file)
        
        print("**     Filename : "+file)
        print("**     Location : "+proDir)
        
        theRawRunFile.retrieveRawMessages()
        theRunHeader=runHeader(theRawRunFile,self.__application.getConfig().getUser()).getHeader()

            
        # process the raw file messages
        #theRawRunRecord=theRawRunFile.retrieveRawMessages()
        
        # get the header for the run
        #theRunHeader=runHeader(theRawRunFile,appConfig.getUser()).getHeader()
        
        # process into the metres version
        #theRunByMetre=runByMetre(theRawRunRecord).processMessages()
        
        # get the records of the run
        #rp=recordProcessor(theRunByMetre)

        