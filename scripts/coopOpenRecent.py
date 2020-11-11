'''
@name:          coopOpenRecent.py
@repository:    https://github.com/studiocoop/maya
@version:       1.5
@license:       UNLICENCE
@author:        Santiago Montesdeoca [artineering.io]

@summary:       Opens the most recent files from a directory within your project 
                with it's default or fixed application (RV, Quicktime, etc)
                Most common uses:
                  -. latest playblasts
                  -. Latest rendered images

@requires:      -

@run:           import coopOpenRecent
                coopOpenRecent.openRecentFile(yourFileFolder='folderInProject', formats=['*.yourFormats'],mostRecentNr=0)
                # 'folderInProject' points to the folder within your Maya project
                # '*.yourFormats' is an array of individual formats
                # 0 means the latest one, the higher the number the less recent the file will be

@created:       16 Nov, 2011
@change:        14 Jul, 2015
'''
import maya.cmds as cmds
import fnmatch
import os

def openRecentFile(yourFileFolder='', formats=['*.mov', '*.avi'], mostRecentNr=0):
    print 'Opening recent file...'
    
    #get path
    path = cmds.workspace(q=True, fullName=True)
    path = os.path.abspath(os.path.join(path, yourFileFolder))#abspath -> normalize path
    print 'Specified path: {0}'.format(path)
    
    #get files and store them in a dict with the time as key
    #also add the keys to a list to later sort them out
    filesDict = dict()
    timeList = []
    for root, dirnames, filenames in os.walk(path):
        for format in formats:
            for filename in fnmatch.filter(filenames, format):
                filePath = os.path.join(root, filename)
                modTime = os.path.getmtime(filePath)
                filesDict[modTime] = filePath
                timeList.append(modTime)

    timeList.sort(reverse=True)
    
    #open the desired file 
    try: 
        recentFile = filesDict[timeList[mostRecentNr]]
        
        print 'File path: {0}'.format(recentFile)
        
        #Open in default program (flexible pipeline)
        import webbrowser
        webbrowser.open(recentFile)
        
        #Open with a defined program (fixed pipeline)
        #import subprocess
        #subprocess.Popen(["C:\\Program Files\\Tweak\\RV-4.0.12-64\\bin\\rv.exe", 'C:\\Users\\Username\\Documents\\maya\\projects\\default\\images\\playblast.mov'])
        
    except:
        cmds.warning('Not enough files to complete your request. {0} Files needed'.format(mostRecentNr+1))
    