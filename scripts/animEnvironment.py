"""
@license:       MIT
@repository:    https://github.com/artineering-io/maya-anim-coop
@summary:       Sets animation environment according to user preferences
@run:           import animEnvironment.py
                animEnvironment.set_hotkeys('default')
                || animEnvironment.set_hotkeys('alt')
                || animEnvironment.reset_hotkeys()
"""
from __future__ import print_function
from __future__ import unicode_literals
import coop.coopLib as lib
import maya.mel as mel
import maya.cmds as cmds
import animPrefs as prefs
import os

hotkeyDict = {
        'default': [False, 'o', 'a', 'g', 't', 't', 's'],
        'alt': [True, 'o', 'a', 'g', 't', 't', 's'],
    }


def load():
    """ loads animation environment
    TODO: values could be defined in animPrefs """
    print("Loading animation environment presets...")
    # set autoKey
    cmds.autoKeyframe(state=True)
    # set 24fps and playback on all viewports
    cmds.playbackOptions(ps=1.0, v='all')
    # set unlimited undo
    cmds.undoInfo(state=True, infinity=True)
    # set manipulator sizes
    if lib.checkAboveVersion(2014):
        cmds.manipOptions(r=False, hs=55, ls=4, sph=1)
    else:
        cmds.manipOptions(r=False, hs=55, ls=4)
    # set frame rate visibility
    mel.eval("setFrameRateVisibility(1);")
    # gimbal rotation
    cmds.manipRotateContext('Rotate', e=True, mode=2)
    # world translation
    cmds.manipMoveContext('Move', e=True, mode=2)
    # time slider height
    playback_slider = mel.eval('$tmpVar=$gPlayBackSlider')
    cmds.timeControl(playback_slider, h=45, e=True)
    # special tick color
    cmds.displayRGBColor("timeSliderTickDrawSpecial", 1, 0.5, 0)

    # check if hotkeys have been set
    if cmds.hotkey('t', ctl=True, query=True, name=True) == 'CharacterAnimationEditorNameCommand':
        print("Hotkeys have been previously loaded")
    else:
        set_hotkeys('default')

    # ask if shelves and plugins should be unloaded
    result = cmds.confirmDialog(title="Animation Environment",
                                icon="question",
                                message="Would you like to also unload unnecessary plugins and shelves?\n"
                                        "You can restore them anytime by right-clicking on the same tool",
                                button=['Yes', 'No'], defaultButton='No', cancelButton='No', dismissString='No',
                                ma='center')
    if result == "Yes":
        unload_plugins()
        delete_shelves()

    lib.displayInfo("ENVIRONMENT SET")


def set_hotkeys(pref='default'):
    """ set hotkeys according to pref dictionary
    TODO: define hotkeys in userPrefs file instead
    """
    # first reset
    reset_hotkeys()
    hotkeys = hotkeyDict[pref]
    # outliner
    cmds.nameCommand('OutlinerWindowNameCommand', ann='OutlinerWindowNameCommand', c='OutlinerWindow')
    cmds.hotkey(k=hotkeys[1], alt=hotkeys[0], name='OutlinerWindowNameCommand', releaseName='')
    # attribute editor
    cmds.nameCommand('AttributeEditorNameCommand', ann='AttributeEditorNameCommand', c='AttributeEditor')
    cmds.hotkey(k=hotkeys[2], alt=hotkeys[0], name='AttributeEditorNameCommand', rn='')
    # graph editor
    cmds.nameCommand('GraphEditorNameCommand', ann='GraphEditorNameCommand', c='GraphEditor')
    cmds.hotkey(k=hotkeys[3], alt=hotkeys[0], name='GraphEditorNameCommand')
    # tool settings
    cmds.nameCommand('ToolSettingsWindowNameCommand', ann='ToolSettingsWindowNameCommand', c='ToolSettingsWindow')
    cmds.hotkey(k=hotkeys[4], alt=hotkeys[0], name='ToolSettingsWindowNameCommand')
    # trax editor
    cmds.nameCommand('CharacterAnimationEditorNameCommand', ann='CharacterAnimationEditorNameCommand',
                     c='CharacterAnimationEditor')
    cmds.hotkey(k=hotkeys[5], ctl=True, name='CharacterAnimationEditorNameCommand')
    if lib.checkAboveVersion(2015):
        # versions below 2016 don't have shift modifier in hotkey command
        # special key
        cmds.nameCommand('SpecialKeyNameCommand', ann='Set a Special Keyframe',
                         c='python("import coopAnim;coopAnim.key_special()")')
        cmds.hotkey(k=hotkeys[6], alt=True, name='SpecialKeyNameCommand')
        # breakdown key
        cmds.nameCommand('BreakdownKeyNameCommand', ann='Key only keyed attributes',
                         c='python("import coopAnim;coopAnim.key_inbetween()")')
        cmds.hotkey(k=hotkeys[6], sht=True, name='BreakdownKeyNameCommand')
    # curvesel key TODO
    # cmds.nameCommand('ScriptEditorNameCommand', ann='ScriptEditorNameCommand', c='ScriptEditor')
    # cmds.hotkey(k=hotkeys[6], sht=True, name='ScriptEditorNameCommand')
    # script editor
    cmds.nameCommand('ScriptEditorNameCommand', ann='ScriptEditorNameCommand', c='ScriptEditor')
    cmds.hotkey(k='i', alt=True, name='ScriptEditorNameCommand')

    lib.displayInfo(pref + " hotkeys set \nTo change or reset hotkeys, right-click on the same shelf button")


def reset_hotkeys():
    if lib.checkAboveVersion(2015):
        # check if hotkey set exists
        if cmds.hotkeySet('coopAnim', exists=True):
            cmds.hotkeySet('coopAnim', current=True, e=True)
        else:
            cmds.hotkeySet('coopAnim', current=True)

    # RESET HOTKEYS
    # outliner
    cmds.hotkey(k='o', alt=False, name='PolyBrushMarkingMenuNameCommand',
                releaseName='PolyBrushMarkingMenuPopDownNameCommand')
    cmds.hotkey(k='o', alt=True, name='')
    # attribute editor
    cmds.hotkey(k='a', alt=False, name='NameComFit_All_in_Active_Panel_MMenu',
                rn='NameComFit_All_in_Active_Panel_MMenu_release')
    cmds.hotkey(k='a', alt=True, name='artisanToggleWireframe_press')
    # graph editor
    cmds.hotkey(k='g', alt=False, name='NameComRepeat_Last_Menu_Action')
    cmds.hotkey(k='g', alt=True, name='HyperGraph_IncreaseDepth')
    # tool settings
    cmds.hotkey(k='t', alt=False, name='NameComShowManip_Tool')
    cmds.hotkey(k='t', alt=True, name='HyperGraph_DecreaseDepth')
    # trax editor
    cmds.hotkey(k='t', ctl=True, name='NameComUniversalManip')
    if lib.checkAboveVersion(2015):
        # keys are not modified if below 2015
        # special key
        cmds.hotkey(k='s', alt=True, name='NameCom_HIKSetFullBodyKey')
        # breakdown key
        cmds.hotkey(k='s', sht=True, name='KeyframeTangentMarkingMenuNameCommand')
    # curvesel key TODO
    lib.displayInfo("Reverted to default Maya hotkeys\n"
                    "To change or reset hotkeys, right mouse click on the same shelf button")


def delete_shelves():
    """ Unload all unnecessary plugins defined in the userPrefs file """
    # find shelves directory
    shelves_path = lib.Path(lib.getEnvDir()).child("prefs").child("shelves")

    # hide unnecessary shelves
    shelves_dict = prefs.unnecessary_shelves
    # Maya creates all default shelves in prefs only after each has been opened (initialized)
    for shelf in shelves_dict:
        try:
            mel.eval('jumpToNamedShelf("{0}");'.format(shelf))
        except RuntimeError:
            continue
    # all shelves loaded -> save them
    mel.eval('saveAllShelves $gShelfTopLevel;')
    # time to delete them
    for shelf in shelves_dict:
        shelf_path = lib.Path(shelves_path.path).child("shelf_{}".format(shelves_dict[shelf]))
        if shelf_path.exists():
            try:
                mel.eval('deleteShelfTab "{}";'.format(shelf))
            except RuntimeError:
                pass
    # all shelves deleted -> save them
    mel.eval('saveAllShelves $gShelfTopLevel;')
    # return to anim shelf
    mel.eval('jumpToNamedShelf("anim");')


def unload_plugins():
    """ Unload all unnecessary plugins defined in the userPrefs file"""
    # unload unnecessary plugins
    plugins = prefs.unnecessary_plugins
    for plugin in plugins:
        if cmds.pluginInfo(plugin, loaded=True, q=True):
            cmds.unloadPlugin(plugin)
            cmds.pluginInfo(plugin, autoload=False, e=True)


def restore_environment():
    """ Restore to default environment """
    # restore unloaded plugins
    plugins = prefs.unnecessary_plugins
    for plugin in plugins:
        if not (cmds.pluginInfo(plugin, loaded=True, q=True)):
            try:
                cmds.loadPlugin(plugin)
                cmds.pluginInfo(plugin, autoload=True, e=True)
            except RuntimeError:
                lib.printWarning("{0} plugin doesn't exist in this version of Maya".format(plugin))

    # restore default hotkeys
    reset_hotkeys()

    # restore default Maya environment
    # set autoKey
    cmds.autoKeyframe(state=False)
    # set 24fps and playback on all viewports
    cmds.playbackOptions(ps=0.0, v='active')
    # set unlimited undo
    cmds.undoInfo(state=True, infinity=False)
    # set manipulator sizes
    cmds.manipOptions(r=False, hs=35, ls=1.0, sph=1)
    # set frame rate visibility
    mel.eval("setFrameRateVisibility(0);")
    # gimbal rotation
    cmds.manipRotateContext('Rotate', e=True, mode=0)
    # world translation
    cmds.manipMoveContext('Move', e=True, mode=0)
    # time slider height
    playback_slider = mel.eval('$tmpVar=$gPlayBackSlider')
    cmds.timeControl(playback_slider, h=36, e=True)
    # special tick color
    cmds.displayRGBColor("timeSliderTickDrawSpecial", 1, 1, 0)

    # restore shelves marked as *.deleted
    lib.restoreShelves()
