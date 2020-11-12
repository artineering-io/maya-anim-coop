"""
@license:       MIT
@repository:    https://github.com/artineering-io/maya-anim-coop
@summary:       One file to rule them all
@run:           import coopPrefs as prefs
"""
from __future__ import unicode_literals

###############################################################################
"""ANIMATION PREFERENCES"""
###############################################################################
# camera settings
default_camera = 'shotcam'
safe_title = False
safe_action = False
resolution_gate = False
display_resolution = False

unnecessary_shelves = {
            'XGen': 'XGen.mel',  # Maya 2015+
            'Sculpting': 'Sculpting.mel',  # Maya 2016+
            'FX Caching': 'FXCaching.mel',  # Maya 2016+
            'FX': 'FX.mel',  # Maya 2016+
            'MASH': 'MASH.mel',  # Maya 2017+
            'Bifrost': 'Bifrost.mel',  # Maya 2017+
            'MotionGraphics': 'MotionGraphics.mel',  # Maya 2017+
            'TURTLE': 'TURTLE.mel'  # Maya 2018+
}

unnecessary_plugins = [
            'hairPhysicalShader',  # Maya 2017+
            'bifrostshellnode',  # Maya 2018+
            'bifrostGraph',  # Maya 2018+
            'bifrostvisplugin',  # Maya 2017+
            'xgenToolkit',  # Maya 2015+
            'MASH'  # Maya 2017+
            'Boss'  #
]

###############################################################################
"""PLAYBLAST PREFERENCES"""
###############################################################################
# movie file settings
playblast_dir = 'movies/'
playblast_format = 'qt'
playblast_resolution = [1280, 720]
playblast_overwrite = True
playblast_HUD = False
playblast_open_file = True
# camera settings
playblast_default_camera = ''
playblast_safe_title = True
playblast_safe_action = True
playblast_resolution_gate = False
playblast_display_resolution = False
