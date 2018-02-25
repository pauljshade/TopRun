'''
Created on 1 Feb 2018

@author: paulj
'''
import toprun
from toprun import fitnessFile, runHeader, runByMetre, recordProcessor

# create the application
toprunApp=toprun.application()

# retrieve the configuration - FOR NOW
appConfig=toprunApp.getConfig()

# show menu
exitFlag=False

while not(exitFlag) :
    toprunApp.getMenu().showMainMenu()

file='C:\\Users\\paulj\\Dropbox\\Apps\\tapiriik\\2474750842.fit'

theRawRunFile=fitnessFile(file)

# process the raw file messages
theRawRunRecord=theRawRunFile.retrieveRawMessages()

# get the header for the run
theRunHeader=runHeader(theRawRunFile,appConfig.getUser()).getHeader()

# process into the metres version
theRunByMetre=runByMetre(theRawRunRecord).processMessages()

# get the records of the run
rp=recordProcessor(theRunByMetre)

# check fastest times
measures=[100,200,400,800,805,1000,1500,1609,3000,5000,8047,10000,15000,16093,20000,21087,24140,25000,30000,32187,35000,40000,42195]
theRunRecords={}
for item in measures :
    rec=rp.getRecord(item)
    theRunRecords['d'+str(item)]=rec

print('User : '+theRunHeader['user']+' Start : '+theRunHeader['startTime']+' Distance : '+str(theRunHeader['totalMetres'])+'m '+' Time : '+str(theRunHeader['totalSeconds'])+'s')
for mitem in measures :
    dl='d'+str(mitem)
    if len(theRunRecords[dl])>0 :
        h=theRunRecords[dl][0]['sec']//3600
        m=(theRunRecords[dl][0]['sec']-3600*h)//60
        s=(theRunRecords[dl][0]['sec']-3600*h-60*m)
        
        print('%05dm : %02.0fh %02.0fm %05.2fs' % (mitem,h,m,s))
        
        
    
    
    



