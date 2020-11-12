"""
@license:       MIT
@repository:    https://github.com/artineering-io/maya-anim-coop
@summary:       Toggles, creates and deletes motion trails of selected objects
@run:           import animMotionTrailToggler
                animMotionTrailToggler.toggleTrails()
                || animMotionTrailToggler.deleteTrails()
                || animMotionTrailToggler.createTrails()
"""
from __future__ import print_function
from __future__ import unicode_literals
import maya.mel as mel
import maya.cmds as cmds


def toggle_trails():
    """ Toggles ghosting attribute on selected shapes """
    # get all selected objects
    sel = cmds.ls(sl=True)
    trails_exists = exist_trails(sel)
    if trails_exists:
        delete_trails(sel)
    else:
        create_trails(sel)


def delete_trails(sel=None):
    """Deletes motion trails on selected nodes"""
    if not sel:
        # get selected nodes
        sel = cmds.ls(sl=True)
    for selected in sel:
        m_trail = cmds.listConnections(selected, t='motionTrail')
        if m_trail:
            cmds.delete('{0}*'.format(m_trail[0]))
        else:
            # check if a motion trail handle is selected
            splitter = selected.split('Handle.')
            if cmds.objectType(splitter[0], isType="motionTrail"):
                cmds.delete("{}*".format(splitter[0]))


def create_trails(sel=None):
    """Creates motion trails on selected nodes"""
    if not sel:
        # get selected nodes
        sel = cmds.ls(sl=True)
        
    # delete existing motion trails
    delete_trails(sel)
    
    # see if time range has been selected
    playback_slider = mel.eval('$tmpVar=$gPlayBackSlider')
    start, end = cmds.timeControl(playback_slider, q=True, rangeArray=True)
    if end-start != 1:
        s_time = start
        e_time = end
    else:
        # no selection done, get min and max playback values
        s_time = cmds.playbackOptions(q=True, min=True)
        e_time = cmds.playbackOptions(q=True, max=True)
    
    # create new trails
    cmds.snapshot(motionTrail=True, increment=1, startTime=s_time, endTime=e_time)
        

def exist_trails(sel):
    """ Returns True if motion trails exist on most of selected objects """
    total_selected = len(sel)
    motion_trails = 0
    for selected in sel:
        if cmds.listConnections(selected, t='motionTrail'):
            motion_trails += 1
        else:
            # check if a motion trail handle is selected
            splitter = selected.split('Handle.')
            print("While checking motion trails, {0}".format(splitter[0]))
            if cmds.objectType(splitter[0], isType="motionTrail"):
                motion_trails += 1
    if motion_trails > (total_selected/2):
        return True
    else: 
        return False
