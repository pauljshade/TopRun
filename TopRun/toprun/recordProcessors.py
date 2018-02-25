'''
Created on 10 Feb 2018

@author: paulj
'''

class recordProcessor(object):
    '''
    classdocs
    '''
    def __init__(self, runByMetre):
        '''
        Constructor
        '''
        
        self.__metreRecord=runByMetre
        
        return
    
    def getRecord(self,distance):
        
        metreRecord=self.__metreRecord
        
        m=len(metreRecord)
        
        theRunRecords=[]

        for i in range(0,m) :
            
            mitem=distance
            lm=mitem
            if i+lm<m :
                dSet={}
                s=metreRecord[i]
                e=metreRecord[i+lm]
                dSet['s']=i
                dSet['e']=i+lm
                dSet['sec']=e['seconds']-s['seconds']
                dSet['dist']=lm
                
                if len(theRunRecords)==0 :
                    theRunRecords.append(dSet)
                else :
                    flag=0
                    for l in range(0,len(theRunRecords)) :
                        if dSet['s']>=theRunRecords[l]['s'] and dSet['s']<=theRunRecords[l]['e'] :
                            if dSet['sec']<theRunRecords[l]['sec'] :
                                del theRunRecords[l]
                                break
                            else :
                                flag=1
                                break
                    if flag==0 :
                        theRunRecords.append(dSet)
        
        return sorted(theRunRecords, key=lambda k: k['sec'])
