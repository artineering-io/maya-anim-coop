"""
@license:       MIT
@repository:    https://github.com/artineering-io/maya-anim-coop
@summary:       Animation utilities
@run:           import coopAnim as cAnim
                cAnim.key_special()
                || cAnim.key_inbetween()
                || cAnim.curve_sel()
"""
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import coop.coopLib as lib


def key_special():
    """ keys selected objects with special color """
    selected = cmds.ls(sl=True)
    for sel in selected:
        cmds.setKeyframe(sel, hierarchy="none", shape=False, an=False)
        time = cmds.currentTime(q=True)
        cmds.keyframe(t=(time, time), e=True, tds=True)


def key_inbetween():
    """ keys inbetweens of selected objects (only selected channels) """
    selected = cmds.ls(sl=True)
    for sel in selected:
        cmds.setKeyframe(sel, hierarchy="none", shape=False, an=True)


def curve_sel():
    """ shows the selected channel of every object in the graph editor """
    # list selection
    sel = cmds.ls(sl=True)
    # save selected attrs of the Graph editor
    sel_obj_attrs = cmds.selectionConnection('graphEditor1FromOutliner', q=True, obj=True)
    if sel_obj_attrs is not None:

        attr_names = []

        # isolate strings of selected attributes
        for curAttr in sel_obj_attrs:
            # if its in an animation layer
            splitter = curAttr.split('_')
            # if the attribute is without "_" it is in no animation layer and we can asume that
            if len(splitter) == 1:
                splitter = curAttr.split('.')
                attr_names.append(splitter[1])
            else:
                # if it has a "_" check if it's because of the attribute name
                splitter = curAttr.split('.')
                attr_splitter = splitter[1].split('_')
                if len(attr_splitter) > 1:
                    attr_names.append(splitter[1])
                    # all cases without animation layers are checked
                else:
                    # it's because it's a nasty animation layer we are dealing with or the objectName has a "_"
                    output = splitter[1]
                    splitter = splitter[0].split('_')
                    length = len(splitter)
                    # if the object has "_" in it's name, iterate through to get attr
                    get_obj_name = False
                    iter_split = 0
                    obj_name = str(splitter[iter_split])
                    while not get_obj_name:
                        for curObj in sel:
                            if str(obj_name) == str(curObj):
                                get_obj_name = True
                                break
                        if not get_obj_name:
                            iter_split += 1
                            obj_name += '_' + str(splitter[iter_split])

                    # the object name is found and the position at which the attribute is found too
                    # print("objectName is {0}".format(objName))

                    if length == (iter_split+1):
                        # it was only the object name that had a "_"
                        attr_names.append(output)
                        continue

                    # if the name of the Animation layer has "_" search that out as well
                    obj_anim_layers = cmds.animLayer(q=True, afl=True)
                    get_layer_name = False
                    back_iter_split = length-1
                    layer_name = str(splitter[back_iter_split])
                    while not get_layer_name:
                        for curLayer in obj_anim_layers:
                            if str(layer_name) == str(curLayer):
                                get_layer_name = True
                                break
                        if not get_layer_name:
                            back_iter_split -= 1
                            layer_name = str(splitter[back_iter_split]) + '_' + str(layer_name)

                    # the layer name is found and the position at which the attribute name will end is found too
                    # print "layerName is {0}".format(layerName)

                    # now get the selected attribute's name
                    iterator = iter_split
                    attr_name = ''
                    while iterator in range(back_iter_split-1):
                        if attr_name:
                            attr_name += '_' + splitter[iterator+1]
                        else:
                            attr_name = splitter[iterator+1]
                        iterator += 1

                    # the rough attribute name has been found
                    # print(attrName)

                    # if it is a rotate attribute, get the coordinate on which it rotates
                    #  maya has it's own naming convention for rotation in animation layers
                    if attr_name == "rotate":
                        end_char = len(str(output))
                        attr_name += str(output)[end_char-1]

                    attr_names.append(attr_name)

        # clear graph selection
        cmds.selectionConnection('graphEditor1FromOutliner', e=True, clear=True)

        # select the attribute for all objects
        for curObj in sel:
            for curAttr in attr_names:
                if cmds.attributeQuery(str(curAttr), node=str(curObj), ex=True):
                    cmds.selectionConnection('graphEditor1FromOutliner', e=True,
                                             select=(str(curObj) + '.' + str(curAttr)))

        # refresh
        # cmds.refresh would only show the ones in the animation layer selected, we want to show all that is selected
        # in the graph editor, even if it's another layer

        # fix graph refresh bug
        cmds.selectKey(str(sel_obj_attrs[0]), add=True)
        cmds.selectKey(clear=True)

    else:
        lib.printWarning("You have not selected any attribute in the Graph Editor or the Attribute selected does not "
                         "have animation")
