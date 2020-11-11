'''
@name:          coopPlayblast.py
@repository:    https://github.com/studiocoop/maya
@version:       0.9
@license:       UNLICENCE
@authors:       Santiago Montesdeoca [artineering.io]

@summary:       playblasts animation with user settings

@requires:      -

@run:           import coopPlayblast
                coopPlayblast.playblast

@created:       15 Aug, 2015
@change:        15 Aug, 2015
'''
#import showSettings as ss
import os
import maya.mel as mel
import maya.cmds as cmds
import userPrefs as prefs
reload(prefs)
import coopModelEditorManager as editor

def playblast():
    selected = cmds.ls(sl=True)
    cmds.select(clear=True)
    #check if current scene is named
    fileName = cmds.file(q=True, sn=True, shn=True)
    if not fileName:
        fileName = "unnamed"
    else:
        fileName = os.path.splitext(fileName)[0]
    print "Playblast will be saved under the following filename: {0}".format(fileName)
    #get camera to playblast from scene
    cameraName = prefs.animDefaultCamera
    print cameraName
    if not cmds.objExists(cameraName):
        #check if there is a camera in a shot file
        cameraName = '*:' + cameraName
        cameras = cmds.ls(cameraName)
        if cameras:
            cameraName = cameras[0]
        else:
            cameraName = cmds.lookThru( q=True )
    print "Playblasting from {0}".format(cameraName),
    cameraShape = cmds.listRelatives(cameraName, s=True)[0]
    cmds.camera(cameraShape, e=True, displaySafeTitle = prefs.playSafeTitle, displaySafeAction = prefs.playSafeAction, displayResolution = prefs.playDisplayResolution)
    #playblast with user settings except ornaments
    editor.hideAllDisplayObjects()
    editor.showOnlyPlayblast()
    #get audio on timeslider
    aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
    audioNode = cmds.timeControl(aPlayBackSliderPython, q=True, s=True)
    #playblast
    cmds.playblast(showOrnaments=prefs.playHUD,  f=prefs.playDir+fileName, format=prefs.playFormat,
    w=prefs.playResolution[0], h=prefs.playResolution[1], percent=100, qlt=70, v=prefs.playOpenFile, fo=prefs.playOverwrite, os=True, s=audioNode)
    cmds.camera(cameraShape, e=True, displaySafeTitle = prefs.animSafeTitle, displaySafeAction = prefs.animSafeAction, displayResolution = prefs.animDisplayResolution)
    #bring back to animation
    editor.showOnlyAnim()
    cmds.select(selected)
