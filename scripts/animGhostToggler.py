"""
@license:       MIT
@repository:    https://github.com/artineering-io/maya-anim-coop
@summary:       Toggles, enables and disables ghosting state of selected objects
@run:           import animGhostToggler
                animGhostToggler.toggle_ghosting()
                || animGhostToggler.disable_ghosting()
                || animGhostToggler.enable_ghosting()
"""
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds


def toggle_ghosting():
    """ Toggles ghosting attribute on selected shapes """
    # get all selected shape nodes
    selected_shapes = cmds.ls(sl=True, s=True, dag=True, lf=True)
    is_enabled = ghosting_enabled(selected_shapes)
    if is_enabled:
        disable_ghosting(selected_shapes)
    else:
        enable_ghosting(selected_shapes)


def disable_ghosting(shapes=None):
    """ Disables ghosting attribute on shapes or selected shapes """
    if not shapes:
        # get selected shape nodes
        shapes = cmds.ls(sl=True, s=True, dag=True, lf=True)
    for shape in shapes:
        cmds.setAttr("{0}.ghosting".format(shape), 0)


def enable_ghosting(shapes=None):
    """ Enables ghosting attribute on shapes or selected shapes """
    if not shapes:
        # get selected shape nodes
        shapes = cmds.ls(sl=True, s=True, dag=True, lf=True)
    for shape in shapes:
        cmds.setAttr("{0}.ghosting".format(shape), 1)


def ghosting_enabled(shapes):
    """ Returns True if ghosting is enabled on most of selected objects """
    total_shapes = len(shapes)
    shapes_with_ghosting = 0
    for shape in shapes:
        shapes_with_ghosting += cmds.getAttr("{0}.ghosting".format(shape))
    if shapes_with_ghosting > (total_shapes/2):
        return True
    else: 
        return False
