import maya.cmds as cmds

#keys selected objects with special color
def keySpecial():
    selected = cmds.ls(sl=True)
    for sel in selected:
        cmds.setKeyframe(sel, hierarchy="none", shape=False, an=False)
        time = cmds.currentTime(q=True)
        cmds.keyframe(t=(time,time), e=True, tds=True)

#keys inbetweens of selected objects (only selected channels)
def keyInbetween():
    selected = cmds.ls(sl=True)
    for sel in selected:
        cmds.setKeyframe(sel, hierarchy="none", shape=False, an=True)

#shows the selected channel of every object in the graph editor
def curveSel():
    #list selection
    sel = cmds.ls(sl=True)
    #save selected attrs of the Graph editor
    curObjAttrs = cmds.selectionConnection('graphEditor1FromOutliner', q=True, obj=True)
    if curObjAttrs != None:

        attrNames = []

        #isolate strings of selected attributes
        for curAttr in curObjAttrs:
            #if its in an animation layer
            splitter = curAttr.split('_')
            #if the attribute is without "_" it is in no animation layer and we can asume that
            if len(splitter)==1:
                splitter = curAttr.split('.')
                attrNames.append(splitter[1])
            else:
                #if it has a "_" check if it's because of the attribute name
                splitter = curAttr.split('.')
                attrSplitter = splitter[1].split('_')
                if len(attrSplitter) > 1:
                    attrNames.append(splitter[1])
                    #all cases without animation layers are checked
                else:
                    #it's because it's a nasty animation layer we are dealing with or the objectName has a "_"
                    output = splitter[1]
                    splitter = splitter[0].split('_')
                    length = len(splitter)
                    #if the object has "_" in it's name, iterate through to get attr
                    getObjName=False
                    iterSplit = 0
                    objName=str(splitter[iterSplit])
                    while getObjName!=True:
                        for curObj in sel:
                            if str(objName) == str(curObj):
                                getObjName=True
                                break
                        if getObjName!=True:
                            iterSplit += 1
                            objName += '_' + str(splitter[iterSplit])

                    #the object name is found and the position at which the attribute is found too
                    #print "objectName is {0}".format(objName)

                    if length == (iterSplit+1):
                        #it was only the object name that had a "_"
                        attrNames.append(output)
                        continue

                    #if the name of the Animation layer has "_" search that out as well
                    objAnimLayers = cmds.animLayer(q=True, afl=True)
                    getLayerName=False
                    backIterSplit = length-1
                    layerName=str(splitter[backIterSplit])
                    while getLayerName!=True:
                        for curLayer in objAnimLayers:
                            if str(layerName) == str(curLayer):
                                getLayerName=True
                                break
                        if getLayerName!=True:
                            backIterSplit -= 1
                            layerName = str(splitter[backIterSplit]) + '_' + str(layerName)

                    #the layer name is found and the position at which the attribute name will end is found too
                    #print "layerName is {0}".format(layerName)

                    #now get the selected attribute's name
                    iterator = iterSplit
                    attrName = ''
                    while iterator in range(backIterSplit-1):
                        if attrName:
                            attrName += '_' + splitter[iterator+1]
                        else:
                            attrName = splitter[iterator+1]
                        iterator +=1

                    #the rough attribute name has been found
                    #print attrName

                    #if it is a rotate attribute, get the coordinate on which it rotates(maya has it's own naming convention for ratation in animation layers)
                    if attrName == "rotate":
                        endChar = len(str(output))
                        attrName += str(output)[endChar-1]

                    attrNames.append(attrName)



        #clear graph selection
        cmds.selectionConnection('graphEditor1FromOutliner', e=True, clear=True)

        #select the attribute for all objects
        for curObj in sel:
            for curAttr in attrNames:
                if (cmds.attributeQuery(str(curAttr), node=str(curObj), ex=True)):
                    cmds.selectionConnection('graphEditor1FromOutliner', e=True, select=(str(curObj) + '.' + str(curAttr)))


        #refresh
        #cmds.refresh would only show the ones in the animation layer selected, we want to show all that is selected in the graph editor, even if it's another layer

        #fix graph refresh bug
        cmds.selectKey(str(curObjAttrs[0]), add=True)
        cmds.selectKey(clear=True)

    else:
        cmds.warning("You have not selected any attribute in the Graph Editor or the Attribute selected does not have animation")
