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
    # this should throw an exception if we've exhuasted all other possibilities
    import qb


# Qube Farm Submission
class Submit(object):
    def __init__(self):
        self.jobs = []

    def addJob(self, in_job):
        self.jobs.append(in_job)

    def submit(self):
        # listOfSubmittedJobs = qb.submit(listOfJobsToSubmit)
        for job in self.jobs:
            print job['package']


# Qube Job Creation
class Job(object):
    def __init__(self):
        self.qjob = {}
        self.qpackage = {}

        self.MAYAEXEPATH = 'C:/Program Files/Autodesk/Maya2016.5/bin/Render.exe'
        self.NUMPROCESSORS = 10

        self.setupPackage()

    def __str__(self):
        return repr(self.buildJob())

    def buildJob(self):
        self.qjob['name'] = 'Hello World'
        self.qjob['prototype'] = 'cmdrange'

        # # of Instances/Computers
        self.qjob['cpus'] = 1

        self.qjob['priority'] = 9999
        self.qjob['reservations'] = 'host.processors=%s' % str(self.NUMPROCESSORS)

        self.qjob['package'] = self.qpackage

        # Using the given range, we will create an agenda list using qb.genframes
        agenda = qb.genchunks(self.qpackage['rangeChunkSize'], self.qpackage['range'])

        # Now that we have a properly formatted agenda, assign it to the job
        self.qjob['agenda'] = agenda

        return self.qjob

    def setupPackage(self):
        package = {}

        self.qpackage['simpleCmdType'] = 'Maya BatchRender (rman)'

        # self.qpackage['-cam'] = 'test'

        self.qpackage['-n'] = str(self.NUMPROCESSORS)

        self.qpackage['-proj'] = 'X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test'

        self.qpackage['-renderer'] = 'rman'
        # self.qpackage['-rl'] = 'test'

        self.qpackage['cmdline'] = '"C:/Program Files/Autodesk/Maya2016.5/bin/Render.exe" -s QB_FRAME_START -e QB_FRAME_END -b QB_FRAME_STEP -n 20 -proj "X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test" -renderer rman "X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test\scenes\Renderfarm_PRman_Simple.ma"'

        self.qpackage['mayaExe'] = self.MAYAEXEPATH

        self.qpackage['range'] = '1-10'
        self.qpackage['rangeChunkSize'] = '5'

        self.qpackage['scenefile'] = 'X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test\scenes\Renderfarm_PRman_Simple.ma'


# Return the Renderable Camera
# def getRenderCamera(filepath):
#     numcams = 0
#     with open(filepath) as fileobj:
#         for line in fileobj:
#             if line.startswith("createNode camera -n"):
#                 numcams += 1
#     print numcams
#
#     fp = open(filepath)
#
#     index = 0
#     while index < numcams:
#         line = fp.next()
#         if line.startswith("createNode camera -n"):
#             while len(line.rstrip().expandtabs(4)) - len(line.rstrip().lstrip()) != 4:
#                 line = fp.next()
#                 # if line.startswith('setAttr ".rnd" no;"'):
#                 #     break
#                 # else:
#                 #     print(line)
#                 #     break
#                 print(line)
#             index += 1
#
#     # Base Line Length
#     # print(line.rstrip().expandtabs(4))
#     # print(line.rstrip().lstrip())
#     # print(len(line.rstrip().expandtabs(4)) - len(line.rstrip().lstrip()))
#     # fp.close()


def returnCamera(filepath):
    # MAKE SURE TO REPLACE PY PATH WITH SERVER PATH
    help = subprocess.Popen(["C:\\Program Files\\Autodesk\\Maya2016.5\\bin\\mayapy.exe", "C:\\Users\\imh29\\Desktop\\QubeSubmit\\qs\\testing.py", filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    camera, err = help.communicate()
    print(camera)


# Return the Render Setting Frame Range
def getFrameRange(filepath):
    fp = open(filepath)
    while True:
        line = fp.next()
        if line.startswith("select -ne :defaultRenderGlobals;"):
            break
    while line.find('".fs"') == -1:
        line = fp.next()
    start = int(line.split(" ")[2].split(";")[0])
    while line.find('".ef"') == -1:
        line = fp.next()
    end = int(line.split(" ")[2].split(";")[0])
    frames = end - start + 1
    print 'frames: %s-%s (%s)' % (start, end, frames)

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
    returnCamera(file)
