#!/usr/bin/python
# -'''- coding: utf-8 -'''-

# As in the last example, we will need the os, sys, and qb modules:
import os, sys

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


# Below is the main function to run in this script
def main():
    # The first few parameters are the same as the previous examples
    job = {}
    job['name'] = 'Python Submission Test 02'
    job['prototype'] = 'cmdrange'

    # Instances
    job['cpus'] = 1
    job['priority'] = 9999
    job['reservations'] = 'host.processors=20'

    # Below creates an empty package dictionary
    package = {}

    # Below instructs the Qube! GUI which submission UI to use for resubmission
    package['simpleCmdType'] = 'Maya BatchRender (rman)'

    # Below defines the camera used for the render
    # package['-cam'] = 'test'

    # Below defines the number of processors the job gets
    package['-n'] = '20'

    # Below defines the project location
    package['-proj'] = 'X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test'

    # Below defines the maya renderer to be used
    package['-renderer'] = 'rman'
    # Below defines the renderlayer to be rendered
    # package['-rl'] = 'test'

    # Below defines the command to be run.  This is necessary for our API submission,
    # but will be re-generate based on user defined parameters upon resubmission.
    package['cmdline'] = '"C:/Program Files/Autodesk/Maya2016.5/bin/Render.exe" -s QB_FRAME_START -e QB_FRAME_END -b QB_FRAME_STEP -n 20 -proj "X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test" -renderer rman "X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test\scenes\Renderfarm_PRman_Simple.ma"'
    # package['cmdline'] = '"/usr/autodesk/maya2016.5/bin/Render" -s QB_FRAME_START -e QB_FRAME_END -b QB_FRAME_STEP -cam "test" -rl "test" -proj "/mnt/storage/" -renderer "rib"  "/mnt/storage/test.mb"'

    # Below defines the maya executable location
    package['mayaExe'] = 'C:/Program Files/Autodesk/Maya2016.5/bin/Render.exe'

    # below defines the range of the job to be rendered
    package['range'] = '1-10'
    package['rangeChunkSize'] = '5'

    # Below defines the scenefile location
    package['scenefile'] = 'X:\Classof2017\imh29\_ToRenderfarm\Renderfarm_PRman_Test\scenes\Renderfarm_PRman_Simple.ma'

    # Below sets the job's package to the package dictionary we just created
    job['package'] = package

    # Using the given range, we will create an agenda list using qb.genframes
    agenda = qb.genchunks(package['rangeChunkSize'], package['range'])

    # Now that we have a properly formatted agenda, assign it to the job
    job['agenda'] = agenda

    listOfJobsToSubmit = []
    listOfJobsToSubmit.append(job)

    print listOfJobsToSubmit[0]

    # As before, we create a list of 1 job, then submit the list.  Again, we
    # could submit just the single job w/o the list, but submitting a list is
    # good form.
    # listOfSubmittedJobs = qb.submit(listOfJobsToSubmit)
    # for job in listOfSubmittedJobs:
    #     print job['id']


# Below runs the "main" function
if __name__ == "__main__":
    main()
    sys.exit(0)
