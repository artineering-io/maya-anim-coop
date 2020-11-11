'''
@name:          coopReplaceMayaEnvironment.py
@repository:    https://github.com/studiocoop/maya
@version:       1.0
@license:       UNLICENCE
@author:        Santiago Montesdeoca [artineering.io]

@summary:       replaces the existing Maya.env with a template which has to
                be in the same directory as this file and hides specified shelves

@requires:      -

@run:           MEL:     python("execfile('E:/coopReplaceMayaEnvironment.py')")
                PYTHON:  execfile('E:/coopReplaceMayaEnvironment.py')

@created:       8 Jul, 2015
@change:        8 Aug, 2016
'''
import os
import maya.mel as mel
import maya.cmds as cmds
import userPrefs as prefs

#find environment directory
scriptsDir = os.path.abspath(cmds.internalVar(usd=True))
envDir = os.path.dirname(scriptsDir)

#hide unnecessary shelves
shelvesDict = prefs.unnecessaryShelvesForAnim
#Maya creates all default shelves in prefs only after each has been opened (initialized)
for shelf in shelvesDict:
    try:
        mel.eval('jumpToNamedShelf("{0}");'.format(shelf))
    except:
        continue
#all shelves loaded -> save them
mel.eval('saveAllShelves $gShelfTopLevel;')
#time to delete them
shelfTopLevel = mel.eval('$tempMelVar=$gShelfTopLevel') + '|'
for shelf in shelvesDict:
    shelfLayout = shelvesDict[shelf].split('.mel')[0]
    if cmds.shelfLayout(shelfTopLevel + shelfLayout, q=True, ex=True):
        cmds.deleteUI(shelfTopLevel+shelfLayout, layout=True)
#mark them as deleted to avoid startup loading
shelfDir = os.path.join(envDir,'prefs','shelves')
for shelf in shelvesDict:
    shelfName = os.path.join(shelfDir,'shelf_' + shelvesDict[shelf])
    deletedShelfName = shelfName + '.deleted'
    if os.path.isfile(shelfName):
        #make sure the deleted file doesn't already exist
        if os.path.isfile(deletedShelfName):
            os.remove(shelfName)
            continue
        os.rename(shelfName,deletedShelfName)

#unload unnecessary plugins
plugins = prefs.unnecessaryPluginsForAnim
for plugin in plugins:
    if (cmds.pluginInfo(plugin, loaded=True, q=True)):
        cmds.unloadPlugin(plugin)
        cmds.pluginInfo(plugin, autoload=False, e=True)
