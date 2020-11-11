'''
@name:          animGhostToggler.py
@repository:    https://github.com/studiocoop/maya
@version:       1.0
@license:       UNLICENCE
@author:        Santiago Montesdeoca [artineering.io]

@summary:       Toggles, enables and disables ghosting state of selected objects

@requires:      -

@run:           import animGhostToggler
                animGhostToggler.toggleGhosting()
                || animGhostToggler.disableGhosting()
                || animGhostToggler.enableGhosting()

@created:       14 Jul, 2015
@change:        14 Jul, 2015
'''
import maya.cmds as cmds

def toggleGhosting():
    '''Toggles ghosting attribute on selected shapes'''
    #get all selected shape nodes
    selectedShapes = cmds.ls(sl=True, s=True, dag=True, lf=True)
    ghostingEnabled = isGhostingEnabled(selectedShapes)
    if ghostingEnabled:
        #disable ghosting
        disableGhosting(selectedShapes)
    else:
        #enable ghosting
        enableGhosting(selectedShapes)


def disableGhosting(shapes=None):
    '''Disables ghosting attribute on shapes or selected shapes'''
    if not shapes:
        #get selected shape nodes
        shapes = cmds.ls(sl=True, s=True, dag=True, lf=True)
    for shape in shapes:
        cmds.setAttr('{0}.ghosting'.format(shape), 0)


def enableGhosting(shapes=None):
    '''Enables ghosting attribute on shapes or selected shapes'''
    if not shapes:
        #get selected shape nodes
        shapes = cmds.ls(sl=True, s=True, dag=True, lf=True)
    selectedShapes = cmds.ls(sl=True, s=True, dag=True, lf=True)
    for shape in selectedShapes:
        cmds.setAttr('{0}.ghosting'.format(shape), 1)


def isGhostingEnabled(shapes):
    '''Returns True if ghosting is enabled on most of selected objects'''
    totalShapes = len(shapes)
    shapesWithGhosting = 0
    for shape in shapes:
        shapesWithGhosting += cmds.getAttr('{0}.ghosting'.format(shape))
    if shapesWithGhosting>(totalShapes/2):
        return True
    else: 
        return False


    
    