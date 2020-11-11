'''
@name:          animEnvironment.py
@repository:    https://github.com/studiocoop/maya
@version:       1.0
@license:       UNLICENCE
@authors:       Santiago Montesdeoca [artineering.io]

@summary:       Sets animation environment according to user preferences

@requires:      -

@run:           import animEnvironment.py
                animEnvironment.setHotkeys('default')
                || animEnvironment.setHotkeys('alt')
                || animEnvironment.resetHotkeys()

@created:       1 Jul, 2015
@change:        19 Jun, 2016
'''
import coopLib as lib
import maya.mel as mel
import maya.cmds as cmds
import userPrefs as prefs

hotkeyDict = {
        'default': [False,'o','a','g','t','t','s'],
        'alt': [True,'o','a','g','t','t','s'],
    }


def load():
    '''loads animation environment'''
    print "loading animation environment presets..."
    #set autoKey
    cmds.autoKeyframe( state=True )
    #set 24fps and playback on all viewports
    cmds.playbackOptions(ps=1.0, v='all')
    #set unlimited undo's
    cmds.undoInfo( state=True, infinity=True )
    #set manipulator sizes
    if lib.checkAboveVersion(2014):
        cmds.manipOptions( r=False, hs=55, ls=4, sph=1 )
    else:
        cmds.manipOptions( r=False, hs=55, ls=4 )
    #set framerate visibility
    mel.eval("setFrameRateVisibility(1);")
    #gimbal rotation
    cmds.manipRotateContext('Rotate', e=True, mode=2)
    #world translation
    cmds.manipMoveContext('Move', e=True, mode=2)
    #time slider height
    aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
    cmds.timeControl(aPlayBackSliderPython, h=45, e=True);
    #special tick color
    cmds.displayRGBColor("timeSliderTickDrawSpecial", 1,0.5,0)

    #check if hotkeys have been set
    if (cmds.hotkey( 't', ctl=True, query=True, name = True)== 'CharacterAnimationEditorNameCommand'):
        print "Hotkeys have been previously loaded"
    else:
        setHotkeys('default')

    print "ENVIRONMENT SET\n", #the comma forces output on the status line


def setHotkeys(pref):
    '''set hotkeys according to pref dictionary'''
    #first reset
    resetHotkeys()
    hotkeys = hotkeyDict[pref]
    #outliner
    cmds.nameCommand( 'OutlinerWindowNameCommand', ann='OutlinerWindowNameCommand', c='OutlinerWindow')
    cmds.hotkey( k=hotkeys[1], alt=hotkeys[0], name='OutlinerWindowNameCommand', releaseName='')
    #attribute editor
    cmds.nameCommand( 'AttributeEditorNameCommand', ann='AttributeEditorNameCommand', c='AttributeEditor')
    cmds.hotkey( k=hotkeys[2], alt=hotkeys[0], name='AttributeEditorNameCommand', rn='')
    #graph editor
    cmds.nameCommand( 'GraphEditorNameCommand', ann='GraphEditorNameCommand', c='GraphEditor')
    cmds.hotkey( k=hotkeys[3], alt=hotkeys[0], name='GraphEditorNameCommand' )
    #tool settings
    cmds.nameCommand( 'ToolSettingsWindowNameCommand', ann='ToolSettingsWindowNameCommand', c='ToolSettingsWindow')
    cmds.hotkey( k=hotkeys[4], alt=hotkeys[0], name='ToolSettingsWindowNameCommand' )
    #trax editor
    cmds.nameCommand( 'CharacterAnimationEditorNameCommand', ann='CharacterAnimationEditorNameCommand', c='CharacterAnimationEditor')
    cmds.hotkey( k=hotkeys[5], ctl=True, name='CharacterAnimationEditorNameCommand' )
    if lib.checkAboveVersion(2015):
        #versions below 2016 don't have shift modifier in hotkey command
        #special key
        cmds.nameCommand( 'SpecialKeyNameCommand', ann='Set a Special Keyframe', c='python("import coopAnimUtils;coopAnimUtils.keySpecial()")')
        cmds.hotkey( k=hotkeys[6], alt=True, name='SpecialKeyNameCommand' )
        #breakdown key
        cmds.nameCommand( 'BreakdownKeyNameCommand', ann='Key only keyed attributes', c='python("import coopAnimUtils;coopAnimUtils.keyInbetween()")')
        cmds.hotkey( k=hotkeys[6], sht=True, name='BreakdownKeyNameCommand' )
    #curvesel key TODO
    #cmds.nameCommand( 'ScriptEditorNameCommand', ann='ScriptEditorNameCommand', c='ScriptEditor')
    #cmds.hotkey( k=hotkeys[6], sht=True, name='ScriptEditorNameCommand' )
    #script editor
    cmds.nameCommand( 'ScriptEditorNameCommand', ann='ScriptEditorNameCommand', c='ScriptEditor')
    cmds.hotkey( k='i', alt=True, name='ScriptEditorNameCommand' )

    print pref + " hotkeys set (to change or reset hotkeys, right mouse click on the same shelf button\n",



def resetHotkeys():

    if lib.checkAboveVersion(2015):
        #check if hotkeyset exists
        if cmds.hotkeySet('coopAnim', exists=True):
            cmds.hotkeySet('coopAnim', current=True, e=True)
        else:
            cmds.hotkeySet( 'coopAnim', current=True )


    '''reset hotkeys'''
    #outliner
    cmds.hotkey( k='o', alt=False, name='PolyBrushMarkingMenuNameCommand', releaseName='PolyBrushMarkingMenuPopDownNameCommand')
    cmds.hotkey( k='o', alt=True, name='' )
    #attribute editor
    cmds.hotkey( k='a', alt=False, name='NameComFit_All_in_Active_Panel_MMenu', rn='NameComFit_All_in_Active_Panel_MMenu_release' )
    cmds.hotkey( k='a', alt=True, name='artisanToggleWireframe_press' )
    #graph editor
    cmds.hotkey( k='g', alt=False, name='NameComRepeat_Last_Menu_Action' )
    cmds.hotkey( k='g', alt=True, name='HyperGraph_IncreaseDepth' )
    #tool settings
    cmds.hotkey( k='t', alt=False, name='NameComShowManip_Tool' )
    cmds.hotkey( k='t', alt=True, name='HyperGraph_DecreaseDepth' )
    #trax editor
    cmds.hotkey( k='t', ctl=True, name='NameComUniversalManip' )
    if lib.checkAboveVersion(2015):
        #keys are not modified if below 2015
        #special key
        cmds.hotkey( k='s', alt=True, name='NameCom_HIKSetFullBodyKey' )
        #breakdown key
        cmds.hotkey( k='s', sht=True, name='KeyframeTangentMarkingMenuNameCommand' )
    #curvesel key TODO
    #
    print "reverted to default maya hotkeys (to change or reset hotkeys, right mouse click on the same shelf button\n",



def restoreShelves():
    #restore unloaded plugins
    plugins = prefs.unnecessaryPluginsForAnim
    for plugin in plugins:
        if not (cmds.pluginInfo(plugin, loaded=True, q=True)):
            try:
                cmds.loadPlugin(plugin)
                cmds.pluginInfo(plugin, autoload=True, e=True)
            except:
                print "{0} plugin doesn't exist in this version of Maya".format(plugin)
    #restoren shelves marked as *.deleted
    lib.restoreShelves()