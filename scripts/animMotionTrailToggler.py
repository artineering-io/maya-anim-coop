'''
@name:          animMotionTrailToggler.py
@version:       1.1
@license:       coop
@author:        Santiago Montesdeoca [studio.coop]
@website:       artineering.io

@summary:       Toggles, creates and deletes motion trails of selected objects

@requires:      -

@run:           import animMotionTrailToggler
                animMotionTrailToggler.toggleTrails()
                || animMotionTrailToggler.deleteTrails()
                || animMotionTrailToggler.createTrails()

@created:       15 Jul, 2015
@change:        23 Oct, 2015
'''
import maya.mel as mel
import maya.cmds as cmds

def toggleTrails():
    '''Toggles ghosting attribute on selected shapes'''
    #get all selected objects
    sel = cmds.ls(sl=True)
    motionTrailExists = doMotionTrailsExist(sel)
    if motionTrailExists:
        #delete motion trails
        deleteTrails(sel)
    else:
        #create motion trails
        createTrails(sel)


def deleteTrails(sel=None):
    '''Deletes motion trails on selected nodes'''
    if not sel:
        #get selected nodes
        sel = cmds.ls(sl=True)
    for selected in sel:
        mTrail = cmds.listConnections(selected, t='motionTrail' )
        if mTrail:
            cmds.delete('{0}*'.format(mTrail[0]))
        else:
            #check if a motion trail handle is selected
            splitter = selected.split('Handle.')
            if cmds.objectType(splitter[0], isType="motionTrail"):
                cmds.delete("{}*".format(splitter[0]))
                


def createTrails(sel=None):
    '''Creates motion trails on selected nodes'''
    if not sel:
        #get selected nodes
        sel = cmds.ls(sl=True)
        
    #delete existing motion trails
    deleteTrails(sel)
    
    #see if time range has been selected
    playBackSlider = mel.eval('$tmpVar=$gPlayBackSlider')
    start, end = cmds.timeControl(playBackSlider, q=True, rangeArray=True)
    if (end-start!=1):
        sTime = start
        eTime = end
    else:
        #no selection done, get min and max playback values
        sTime = cmds.playbackOptions(q=True, min=True)
        eTime = cmds.playbackOptions(q=True, max=True)
    
    #create new trails
    cmds.snapshot(motionTrail=True, increment=1, startTime=sTime, endTime=eTime)
        


def doMotionTrailsExist(sel):
    '''Returns True if motion trails exist on most of selected objects'''
    totalSelected = len(sel)
    motionTrails = 0
    for selected in sel:
        if cmds.listConnections(selected, t='motionTrail' ):
            motionTrails+=1;
        else:
            #check if a motion trail handle is selected
            splitter = selected.split('Handle.')
            print "While checkong motion trails, {0}".format(splitter[0])
            if cmds.objectType(splitter[0], isType="motionTrail"):
                motionTrails+=1;
    if motionTrails>(totalSelected/2):
        return True
    else: 
        return False


    
    