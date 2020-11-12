"""
@license:       MIT
@repository:    https://github.com/artineering-io/maya-anim-coop
@summary:       Opens the most recent files from a directory within your project
                with it's default or fixed application (RV, Quicktime, etc)
                Most common uses:
                  -. latest playblasts
                  -. Latest rendered images
@run:           import coopOpenRecent
                coopOpenRecent.open_recent(project_folder='folderInProject', formats=['*.yourFormats'],
                                           most_recent_nr=0)
                # 'folderInProject' points to the folder within your Maya project
                # '*.yourFormats' is an array of individual formats
                # 0 means the latest one, the higher the number the less recent the file will be
"""
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import fnmatch
import os


def open_recent(project_folder="", formats=None, most_recent_nr=0):
    if formats is None:
        formats = ['*.mov', '*.avi']
    print("Opening recent file...")
    
    # get path
    path = cmds.workspace(q=True, fullName=True)
    path = os.path.abspath(os.path.join(path, project_folder))  # abspath -> normalize path
    print("Specified path: {0}".format(path))
    
    # get files and store them in a dict with the time as key
    # also add the keys to a list to later sort them out
    files_dict = dict()
    time_list = []
    for root, dirnames, filenames in os.walk(path):
        for f in formats:
            for filename in fnmatch.filter(filenames, f):
                file_path = os.path.join(root, filename)
                mod_time = os.path.getmtime(file_path)
                files_dict[mod_time] = file_path
                time_list.append(mod_time)

    time_list.sort(reverse=True)
    
    # open the desired file
    try: 
        recent_file = files_dict[time_list[most_recent_nr]]
        
        print("File path: {0}".format(recent_file))
        
        # Open in default program (flexible pipeline)
        import webbrowser
        webbrowser.open(recent_file)
        
        # Open with a defined program (fixed pipeline)
        # import subprocess
        # subprocess.Popen(["C:\\Program Files\\Tweak\\RV-4.0.12-64\\bin\\rv.exe",
        #                   'C:\\Users\\Username\\Documents\\maya\\projects\\default\\images\\playblast.mov'])
        
    except RuntimeError:
        cmds.warning('Not enough files to complete your request. {0} Files needed'.format(most_recent_nr + 1))
