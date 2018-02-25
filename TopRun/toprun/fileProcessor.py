'''
Created on 10 Feb 2018

@author: paulj
'''

from fitparse import FitFile

class fitnessFile(object):
    '''
    classdocs
    '''
    
    # class members
    # fileLocation : disk location of original files
    # measureList  : list of currently supported file measures
    # rawRunRecord : list of track points from the raw records

    def __init__(self, fileLocation):
        '''
        Constructor
        '''
        self.__fileLocation=fileLocation
        self.__fitFile=FitFile(self.__fileLocation)
        
        self.__rawRunRecord=[]
        
        self.__measureList=['distance','timestamp','heart_rate','activity_type']
        self.__allKeys=[]
        
        return
    
    def retrieveRawMessages(self):
    
        # Get all data messages that are of type record
        for record in self.__fitFile.get_messages('record'):
    
            point={}    
            # Go through all the data entries in this record
            for record_data in record:
                self.__allKeys.append(record_data.name)
                
                if record_data.name in self.__measureList :            
                    point[record_data.name]=record_data.value

            self.__rawRunRecord.append(point)
            
            self.__allKeys=list(set(self.__allKeys))
                
        return self.__rawRunRecord
    
    def getAllkeys(self):
        return self.__allKeys
    
    def getMessages(self):
        return self.__rawRunRecord
    
    