"""
@license:       MIT
@repository:    https://github.com/artineering-io/maya-anim-coop
@summary:       manages model editor panels (3D-viewports) settings for specific tasks
                - showOnlyAnim
                - showOnlyLayout
                - showOnlyPlayblast
@run:           import coopModelEditorManager
                coopModelEditorManager.show_only_anim()
                || coopModelEditorManager.show_only_layout()
                || coopModelEditorManager.show_only_playblast()
"""
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import coop.coopLib as lib


def hide_all(model_panel=None):
    """ hides all display objects of modelPanel """
    if not model_panel:
        model_panel = lib.getActiveModelPanel()
    cmds.modelEditor(model_panel, e=True, alo=False)


def show_only_anim():
    """ show only nurbs (surfaces, curves) and polys (smoothshaded) """
    activ_model_panel = lib.getActiveModelPanel()
    if activ_model_panel:
        hide_all(activ_model_panel)
        cmds.modelEditor(activ_model_panel, e=True, ns=True)  # nurbs surfaces
        cmds.modelEditor(activ_model_panel, e=True, nc=True)  # nurbs curves
        cmds.modelEditor(activ_model_panel, e=True, pm=True)  # polygons
        cmds.modelEditor(activ_model_panel, e=True, motionTrails=True)  # motion trails
        cmds.modelEditor(activ_model_panel, e=True, greasePencils=True)  # grease pencil
        cmds.modelEditor(activ_model_panel, e=True, displayAppearance='smoothShaded')
    else:
        cmds.warning("No active model panel"),

        
def show_only_layout():
    """ show only nurbs, polys (flatshaded) and cameras """
    activ_model_panel = lib.getActiveModelPanel()
    if activ_model_panel:
        hide_all(activ_model_panel)
        cmds.modelEditor(activ_model_panel, e=True, ns=True)  # nurbs surfaces
        cmds.modelEditor(activ_model_panel, e=True, pm=True)  # polygons
        cmds.modelEditor(activ_model_panel, e=True, ca=True)  # cameras
        cmds.modelEditor(activ_model_panel, e=True, motionTrails=True)  # motion trails
        cmds.modelEditor(activ_model_panel, e=True, greasePencils=True)  # grease pencil
        cmds.modelEditor(activ_model_panel, e=True, displayAppearance='flatShaded')
    else:
        cmds.warning("No active model panel"),
        
            
def show_only_playblast():
    """ show only geometry (smoothShaded) """
    activ_model_panel = lib.getActiveModelPanel()
    if activ_model_panel:
        hide_all(activ_model_panel)
        cmds.modelEditor(activ_model_panel, e=True, ns=True)  # nurbs surfaces
        cmds.modelEditor(activ_model_panel, e=True, pm=True)  # polygons
        cmds.modelEditor(activ_model_panel, e=True, displayAppearance='smoothShaded')
    else:
        cmds.warning("No active model panel"),


def show_only_rigging():
    activ_model_panel = lib.getActiveModelPanel()
    if activ_model_panel:
        hide_all(activ_model_panel)
        # probably show all?
        cmds.modelEditor(activ_model_panel, e=True, ns=True)  # nurbs surfaces
        cmds.modelEditor(activ_model_panel, e=True, nc=True)  # nurbs curves
        cmds.modelEditor(activ_model_panel, e=True, pm=True)  # polygons
        cmds.modelEditor(activ_model_panel, e=True, j=True)  # joints
        cmds.modelEditor(activ_model_panel, e=True, jx=True)  # x-ray joints
        cmds.modelEditor(activ_model_panel, e=True, ikh=True)  # IK handles
        cmds.modelEditor(activ_model_panel, e=True, df=True)  # deformers
        cmds.modelEditor(activ_model_panel, e=True, dy=True)  # dynamics
        cmds.modelEditor(activ_model_panel, e=True, lc=True)  # locators
        cmds.modelEditor(activ_model_panel, e=True, displayAppearance='smoothShaded')
    else:
        cmds.warning("No active model panel"),
