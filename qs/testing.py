import maya.standalone
maya.standalone.initialize( name='python' )
import maya.cmds as cmd
import sys

def func():
    cameras = cmd.listCameras()
    for index, cam in enumerate(cameras):
        if cmd.getAttr(cam + '.renderable'):
            sys.stdout.write(cam)
            sys.stdout.flush()
            sys.exit(0)

fpath = sys.argv[1]
# fileToOpen = "\\\\awexpress.westphal.drexel.edu\\digm_anfx\\SRPJ_LAW\\working\\scenes\\lpo\\010\\01. PreVis\\lpo_010_FoilBlocking_v05_PreVis_imh29.ma"
cmd.file(fpath, o=True)
func()
