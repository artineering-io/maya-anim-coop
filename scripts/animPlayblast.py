"""
@license:       MIT
@repository:    https://github.com/artineering-io/maya-anim-coop
@summary:       Playblasts animations with user settings
@run:           import coopPlayblast
                coopPlayblast.playblast()
"""
from __future__ import print_function
from __future__ import unicode_literals
import os
import maya.mel as mel
import maya.cmds as cmds
import animPrefs as prefs
import coopModelEditorManager as editor
import coop.coopLib as cLib


def playblast():
    selected = cmds.ls(sl=True)
    cmds.select(clear=True)
    # check if current scene is named
    file_name = cmds.file(q=True, sn=True, shn=True)
    if not file_name:
        file_name = "unnamed"
    else:
        file_name = os.path.splitext(file_name)[0]
    print("Playblast will be saved under the following filename: {0}".format(file_name))
    # get camera to playblast from scene
    camera_name = prefs.default_camera
    print(camera_name)
    if not cmds.objExists(camera_name):
        # check if there is a camera in a shot file
        camera_name = '*:' + camera_name
        cameras = cmds.ls(camera_name)
        if cameras:
            camera_name = cameras[0]
        else:
            camera_name = cmds.lookThru(q=True)
    cLib.printInfo("Playblasting from {0}".format(camera_name))
    camera_shape = cmds.listRelatives(camera_name, s=True)[0]
    cmds.camera(camera_shape, e=True, displaySafeTitle=prefs.playblast_safe_title, displaySafeAction=prefs.playblast_safe_action,
                displayResolution=prefs.playblast_display_resolution)
    # playblast with user settings except ornaments
    editor.hide_all()
    editor.show_only_playblast()
    # get audio on timeslider
    playback_slider = mel.eval('$tmpVar=$gPlayBackSlider')
    audio_node = cmds.timeControl(playback_slider, q=True, s=True)
    # playblast
    cmds.playblast(showOrnaments=prefs.playblast_HUD, f=prefs.playblast_dir + file_name, format=prefs.playblast_format,
                   w=prefs.playblast_resolution[0], h=prefs.playblast_resolution[1], percent=100, qlt=70, v=prefs.playblast_open_file,
                   fo=prefs.playblast_overwrite, os=True, s=audio_node)
    cmds.camera(camera_shape, e=True, displaySafeTitle=prefs.safe_title, displaySafeAction=prefs.safe_action,
                displayResolution=prefs.display_resolution)
    # bring back to animation
    editor.show_only_anim()
    cmds.select(selected)
