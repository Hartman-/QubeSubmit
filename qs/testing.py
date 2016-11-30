import maya.standalone
maya.standalone.initialize( name='python' )
import maya.cmds as cmd
import sys

def frameRange():
    fstart = cmd.getAttr('defaultRenderGlobals.startFrame')
    fend = cmd.getAttr('defaultRenderGlobals.endFrame')
    fstring = '%s-%s' % (int(fstart), int(fend))
    return fstring

def imagePrefix():
    prefix = cmd.getAttr('defaultRenderGlobals.imageFilePrefix')
    return prefix


def renderCam():
    cameras = cmd.listCameras()
    for index, cam in enumerate(cameras):
        if cmd.getAttr(cam + '.renderable'):
            return cam


def main():
    camera = renderCam()
    prefix = imagePrefix()
    frames = frameRange()
    items = [camera, prefix, frames]

    for item in items:
        sys.stdout.write(item)
        sys.stdout.write(" ")

    sys.stdout.flush()
    sys.exit(0)


fpath = sys.argv[1]
# fileToOpen = "\\\\awexpress.westphal.drexel.edu\\digm_anfx\\SRPJ_LAW\\working\\scenes\\lpo\\010\\01. PreVis\\lpo_010_FoilBlocking_v05_PreVis_imh29.ma"
cmd.file(fpath, o=True)
main()
