'''
@name:          coopModelEditorManager.py
@repository:    https://github.com/studiocoop/maya
@version:       1.0
@license:       UNLICENCE
@authors:       Santiago Montesdeoca [artineering.io]

@summary:       manages model editor panels (3D-viewports) settings for specific tasks
                - showOnlyAnim
                - showOnlyLayout
                - showOnlyPlayblast
                - showOnlyRigging (WIP)

@requires:      -

@run:           import coopModelEditorManager
                coopModelEditorManager.showOnlyAnim()
                || coopModelEditorManager.showOnlyLayout()
                || coopModelEditorManager.showOnlyPlayblast()

@created:       14 Jul, 2015
@change:        08 Aug, 2015
'''
import coopLib as lib
import maya.cmds as cmds


def hideAllDisplayObjects(modelPanel=None):
    '''hides all display objects of modelPanel'''
    if not modelPanel:
        modelPanel = lib.getActiveModelPanel()
    cmds.modelEditor(modelPanel, e=True, alo=False)


def showOnlyAnim():
    '''show only nurbs (surfaces, curves) and polys (smoothshaded)'''
    currentModelPanel = lib.getActiveModelPanel()
    if currentModelPanel:
        hideAllDisplayObjects(currentModelPanel)
        cmds.modelEditor(currentModelPanel, e=True, ns=True) #nurbs surfaces
        cmds.modelEditor(currentModelPanel, e=True, nc=True) #nurbs curves
        cmds.modelEditor(currentModelPanel, e=True, pm=True) #polygons
        cmds.modelEditor(currentModelPanel, e=True, motionTrails=True) #motion trails
        cmds.modelEditor(currentModelPanel, e=True, greasePencils=True) #grease pencil
        cmds.modelEditor(currentModelPanel, e=True, displayAppearance='smoothShaded')
    else:
        cmds.warning("No active model panel"),

        
def showOnlyLayout():
    '''show only nurbs, polys (flatshaded) and cameras'''
    currentModelPanel = lib.getActiveModelPanel()
    if currentModelPanel:
        hideAllDisplayObjects(currentModelPanel)
        cmds.modelEditor(currentModelPanel, e=True, ns=True) #nurbs surfaces
        cmds.modelEditor(currentModelPanel, e=True, pm=True) #polygons
        cmds.modelEditor(currentModelPanel, e=True, ca=True) #cameras
        cmds.modelEditor(currentModelPanel, e=True, motionTrails=True) #motion trails
        cmds.modelEditor(currentModelPanel, e=True, greasePencils=True) #grease pencil
        cmds.modelEditor(currentModelPanel, e=True, displayAppearance='flatShaded')
    else:
        cmds.warning("No active model panel"),
        
            
def showOnlyPlayblast():
    '''show only geometry (smoothShaded)'''
    currentModelPanel = lib.getActiveModelPanel()
    if currentModelPanel:
        hideAllDisplayObjects(currentModelPanel)
        cmds.modelEditor(currentModelPanel, e=True, ns=True) #nurbs surfaces
        cmds.modelEditor(currentModelPanel, e=True, pm=True) #polygons
        cmds.modelEditor(currentModelPanel, e=True, displayAppearance='smoothShaded')
    else:
        cmds.warning("No active model panel"),


def showOnlyRigging():
    currentModelPanel = lib.getActiveModelPanel()
    if currentModelPanel:
        hideAllDisplayObjects(currentModelPanel)
        #probably show all?
        cmds.modelEditor(currentModelPanel, e=True, ns=True) #nurbs surfaces
        cmds.modelEditor(currentModelPanel, e=True, nc=True) #nurbs curves
        cmds.modelEditor(currentModelPanel, e=True, pm=True) #polygons
        cmds.modelEditor(currentModelPanel, e=True, j=True) #joints
        cmds.modelEditor(currentModelPanel, e=True, jx=True) #x-ray joints
        cmds.modelEditor(currentModelPanel, e=True, ikh=True) #IK handles
        cmds.modelEditor(currentModelPanel, e=True, df=True) #deformers
        cmds.modelEditor(currentModelPanel, e=True, dy=True) #dynamics
        cmds.modelEditor(currentModelPanel, e=True, lc=True) #locators
        cmds.modelEditor(currentModelPanel, e=True, displayAppearance='smoothShaded')
    else:
        cmds.warning("No active model panel"),
