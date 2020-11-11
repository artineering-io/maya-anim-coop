'''
@name:          coopPrefs.py
@repository:    https://github.com/studiocoop/maya
@version:       0.9
@license:       UNLICENCE
@authors:       Santiago Montesdeoca [artineering.io]

@summary:       One file to rule them all

@requires:      -

@run:           import coopPrefs as prefs

@created:       21 Dec, 2015
@change:        08 Aug, 2016
'''
###############################################################################
'''USER SETUP PREFERENCES'''
###############################################################################
def setup():
    '''This function will run after the tools have been installed, feel free to
    edit this to your desire'''
    import coopReplaceMayaEnvironment


###############################################################################
'''COMPANY PREFERENCES'''
###############################################################################
companyName = 'ADM Animation' #change this to your name or company to brand the tools


###############################################################################
'''ANIMATION PREFERENCES'''
###############################################################################
#camera settings
animDefaultCamera = 'shotcam'
animSafeTitle = False
animSafeAction = False
animResolutionGate = False
animDisplayResolution = False

unnecessaryShelvesForAnim = {
            'Dynamics'       : 'Dynamics.mel', #Maya 2011-2015
            'Fluids'         : 'Fluids.mel', #Maya 2013-2015
            'Fur'            : 'Fur.mel', #Maya 2013-2015
            'Muscle'         : 'Muscle.mel', #Maya 2013-2015
            'nCloth'         : 'NCloth.mel', #Maya 2013-2015
            'Subdivs'        : 'Subdivs.mel', #Maya 2011-2013
            'Toon'           : 'Toon.mel', #Maya 2013-2015
            'nHair'          : 'Hair.mel', #Maya 2013-2015
            'PaintEffects'   : 'PaintEffects.mel', #Maya 2013-2015
            'XGen'           : 'XGen.mel', #Maya 2015+
            'Sculpting'      : 'Sculpting.mel', #Maya 2016+
            'FX Caching'     : 'FXCaching.mel', #Maya 2016+
            'FX'             : 'FX.mel', #Maya 2016+
            'MASH'           : 'MASH.mel', #Maya 2017+
            'Bifrost'        : 'Bifrost.mel', #Maya 2017+
            'Motion Graphics': 'MotionGraphics.mel' #Maya 2017+
}

unnecessaryPluginsForAnim = [
            'hairPhysicalShader', #Maya 2017+
            'bifrostshellnode', #Maya 2017+
            'bifrostvisplugin', #Maya 2017+
            'xgenToolkit', #Maya 2015+
            'MASH' #Maya 2017+
]
###############################################################################
'''PLAYBLAST PREFERENCES'''
###############################################################################
#movie file settings
playDir = 'movies/'
playFormat = 'qt'
playResolution = [1280, 720]
playOverwrite = True
playHUD = False
playOpenFile = True
#camera settings
playDefaultCamera = ''
playSafeTitle = True
playSafeAction = True
playResolutionGate = False
playDisplayResolution = False
