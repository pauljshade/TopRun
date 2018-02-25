'''
Created on 10 Feb 2018

@author: paulj
'''
import hashlib

def timestampToStr(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
def hashmd5(string):
    return hashlib.md5(str(string).encode()).hexdigest()