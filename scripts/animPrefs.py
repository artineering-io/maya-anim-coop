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
            'Dynamics': 'Dynamics.mel',  # Maya 2011-2015
            'Fluids': 'Fluids.mel',  # Maya 2013-2015
            'Fur': 'Fur.mel',  # Maya 2013-2015
            'Muscle': 'Muscle.mel',  # Maya 2013-2015
            'nCloth': 'NCloth.mel',  # Maya 2013-2015
            'Subdivs': 'Subdivs.mel',  # Maya 2011-2013
            'Toon': 'Toon.mel',  # Maya 2013-2015
            'nHair': 'Hair.mel',  # Maya 2013-2015
            'PaintEffects': 'PaintEffects.mel',  # Maya 2013-2015
            'XGen': 'XGen.mel',  # Maya 2015+
            'Sculpting': 'Sculpting.mel',  # Maya 2016+
            'FX Caching': 'FXCaching.mel',  # Maya 2016+
            'FX': 'FX.mel',  # Maya 2016+
            'MASH': 'MASH.mel',  # Maya 2017+
            'Bifrost': 'Bifrost.mel',  # Maya 2017+
            'Motion Graphics': 'MotionGraphics.mel'  # Maya 2017+
}

unnecessary_plugins = [
            'hairPhysicalShader',  # Maya 2017+
            'bifrostshellnode',  # Maya 2017+
            'bifrostvisplugin',  # Maya 2017+
            'xgenToolkit',  # Maya 2015+
            'MASH'  # Maya 2017+
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
