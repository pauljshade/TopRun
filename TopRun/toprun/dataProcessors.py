'''
Created on 10 Feb 2018

@author: paulj
'''
import toprun.utilities as util

class runHeader(object):
    
    def __init__(self,rawRecord,user):
        
        self.__rawRecord=rawRecord
        self.__user=user
        
        return
    
    def getHeader(self): 
           
        theRawRunRecord=self.__rawRecord.getMessages()
        user=self.__user
        
        run={}        
        last=len(theRawRunRecord)-1
        run['activity']=self.__coalesce(theRawRunRecord[last],'activity_type','unknown')
        run['totalMetres']=theRawRunRecord[last]['distance']
        run['totalSeconds']=(theRawRunRecord[last]['timestamp']-theRawRunRecord[0]['timestamp']).total_seconds()
        run['startTime']=util.timestampToStr(theRawRunRecord[0]['timestamp'])
        run['GPSFlag']=self.__gymCheck()
        

        run['user']=util.hashmd5(user)
        
        run['allkeys']=self.__rawRecord.getAllkeys()

        return run
    
    def __coalesce(self,record,key,default):
        if key in record.keys() :
            return record[key]
        else :
            return default
        
    def __gymCheck(self):
        if 'position_lat' in self.__rawRecord.getAllkeys() :
            return 'GPS'
        else :
            return 'NOGPS'
    
class runByMetre(object):
    '''
    classdocs
    '''
    def __init__(self, rawRecord):
        '''
        Constructor
        '''
        self.__rawRecord=rawRecord
        
        return
        
    def processMessages(self):
        
        theRawRunRecord=self.__rawRecord
        
        # list of meters
        theRunByMetre=[]
        
        # metre measure
        m=0

        # set the previous record initially to 0 - first record
        prevTime=theRawRunRecord[0]['timestamp']
        prevDistance=theRawRunRecord[0]['distance']

        # initialise residulas to 0
        resSeconds=0
        resMetres=0
        
        metre={}
        metre['metre']=0
        metre['seconds']=0
        metre['secondsPm']=0
        theRunByMetre.append(metre)

        secCount=0
        
        # loop through the items meter 0 to end
        for item in theRawRunRecord :     
        
            # current record
            time=item['timestamp']
            distance=item['distance']
            
            # distance and time from the last
            newMetres=distance-prevDistance
            newSeconds=(time-prevTime).total_seconds()
            
            #print("Nm:%s Ns:%s Rm:%s Rs:%s" % (newMetres, newSeconds, resMetres, resSeconds))
            #print(item)
        
            (metres,resMetres,resSeconds)=self.calcMetre(m,newMetres,newSeconds,resMetres,resSeconds)
            
            for met in metres :
                m+=1
                secCount+=met['secondsPm']
                met['seconds']=secCount
                theRunByMetre.append(met)
                #print(met)
            
            prevTime=time
            prevDistance=distance
            
        if resMetres+resSeconds>0 :
            metre={}
            metre['metre']=m+1
            metre['seconds']=secCount+resSeconds/resMetres
            metre['secondsPm']=resSeconds/resMetres
            theRunByMetre.append(metre)
            #print(metre)
         
        return sorted(theRunByMetre, key=lambda k: k['metre'])
            
    def calcMetre(self,metreNo,nMetres,nSeconds,rMetres,rSeconds) :
        
        metres=[]
            
        if rMetres+nMetres<1 :
            rMetres+=nMetres
            rSeconds+=nSeconds
        else :
                    
            nSpM=nSeconds/nMetres
            
            while rMetres+nMetres>1 :
                metre={}
                metre['metre']=metreNo+1
    
                metre['secondsPm']=rSeconds+(1-rMetres)*nSpM
                
                nMetres=nMetres+rMetres-1
                nSeconds=nSeconds+rSeconds-metre['secondsPm']
    
                rSeconds=0
                rMetres=0
                metres.append(metre)
                
                metreNo+=1
            
            rMetres=nMetres
            rSeconds=nSeconds
            
        return (metres,rMetres,rSeconds)