#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os, sys
import subprocess

try:
    import qb
except ImportError:
    if os.environ.get("QBDIR"):
        qbdir_api = os.path.join(os.environ.get("QBDIR"), "api", "python")
    for api_path in (qbdir_api,
                     "/Applications/pfx/qube/api/python/",
                     "/usr/local/pfx/qube/api/python/",
                     "C:\\Program Files\\pfx\\qube\\api\\python",
                     "C:\\Program Files (x86)\\pfx\\qube\\api\\python"):
        if api_path not in sys.path and os.path.exists(api_path):
            sys.path.insert(0, api_path)
            try:
                import qb
            except:
                continue
            break


# Qube Farm Submission
class Submit(object):
    def __init__(self):
        self.jobs = []

    def addJob(self, in_job):
        self.jobs.append(in_job)

    def submit(self):
        # qb.submit(self.jobs[0])
        print self.jobs[0]


# Qube Job Creation
class Job(object):
    def __init__(self):
        self.qjob = {}
        self.qpackage = {}

        self.MAYAEXEPATH = 'C:/Program Files/Autodesk/Maya2016.5/bin/Render.exe'

        self.name = ''
        self.insts = 0
        self.priority = 0
        self.proto = str('cmdrange')
        self.ren = ''
        self.procs = 0
        self.proj = ''
        self.imgdir = ''
        self.cam = ''
        self.frange = ''
        self.chunks = 0
        self.scene = ''

    def buildJob(self):

        self.qjob['name'] = self.name
        self.qjob['prototype'] = self.proto

        # # of Instances/Computers
        self.qjob['cpus'] = self.insts

        self.qjob['priority'] = int(self.priority)
        self.qjob['reservations'] = 'host.processors=%s' % str(self.procs)

        self.qjob['package'] = self.qpackage

        # Using the given range, we will create an agenda list using qb.genframes
        agenda = qb.genchunks(self.qpackage['rangeChunkSize'], self.qpackage['range'])

        # Now that we have a properly formatted agenda, assign it to the job
        self.qjob['agenda'] = agenda


    def setupPackage(self):

        self.qpackage['simpleCmdType'] = 'Maya BatchRender (%s)' % self.ren

        self.qpackage['-cam'] = self.cam

        self.qpackage['-n'] = str(self.procs)

        self.qpackage['-proj'] = self.proj
        # 'X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test'

        self.qpackage['-rd'] = self.imgdir

        self.qpackage['-renderer'] = self.ren
        # self.qpackage['-rl'] = 'test'

        # self.qpackage['cmdline'] = '"C:/Program Files/Autodesk/Maya2016.5/bin/Render.exe" -s QB_FRAME_START -e QB_FRAME_END -b QB_FRAME_STEP -n 20 -proj "X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test" -renderer rman "X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test\scenes\Renderfarm_PRman_Simple.ma"'

        self.qpackage['mayaExe'] = self.MAYAEXEPATH

        self.qpackage['range'] = self.frange
        self.qpackage['rangeChunkSize'] = self.chunks

        self.qpackage['scenefile'] = self.scene
        # 'X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test\scenes\Renderfarm_PRman_Simple.ma'

        self.qpackage['cmdline'] = self.buildCmd()
        self.buildJob()

    def buildCmd(self):
        cmd = '"%s" -s QB_FRAME_START -e QB_FRAME_END -b QB_FRAME_STEP -rd %s -cam %s -n %s -proj "%s" -renderer %s "%s"' % (
            self.MAYAEXEPATH,
            self.qpackage['-rd'],
            self.qpackage['-cam'],
            self.qpackage['-n'],
            self.qpackage['-proj'],
            self.ren,
            self.qpackage['scenefile'])
        return cmd


def parseMayaFile(filepath):
    # MAKE SURE TO REPLACE PY PATH WITH SERVER PATH
    userPath = r'%s' % os.path.expanduser('~')
    cmd = ["C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\mayapy.exe", "X:\\Classof2017\\imh29\\_cmds\\MayaParse.py", filepath]
    help = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=userPath)
    ret, err = help.communicate()

    print(err)

    returnObjects = ret.split(" ")
    returnObjects.pop()
    print(returnObjects)
    return returnObjects


# TESTING
if __name__ == "__main__":
    # myJob = Job()
    #
    # print(myJob)
    # sys.exit(0)

    # QSubmit = Submit()
    # QSubmit.addJob(myJob)
    # QSubmit.submit()
    file = "\\\\awexpress.westphal.drexel.edu\\digm_anfx\\SRPJ_LAW\\working\\scenes\\lpo\\010\\01. PreVis\\lpo_010_FoilBlocking_v05_PreVis_imh29.ma"
    test = parseMayaFile(file)