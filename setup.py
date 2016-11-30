from distutils.core import setup
import py2exe

setup(
    name='QubeSubmit',
    version='0.1.0',
    description='Qube Submission GUI',
    author='Ian Hartman',
    options={
        "py2exe": {
            "dll_excludes": ["MSVCP90.dll"]
        }
    },
    windows=['qs/core.py'])
