#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *

from qs.gui import HorizLine, VertLine, HLineItem, HLineList, FileDrop, HTable, ListDrop
from qs.internal import Job, Submit, parseMayaFile, getWorkers


class TabLayout(QTabWidget):

    logStatus = Signal(str)

    def __init__(self, parent=None):
        super(TabLayout, self).__init__(parent)

        # -------------------------------------------------------------------------------------------------------------

        self.tab_JobInfo = QWidget()
        self.tab_SceneInfo = QWidget()
        self.tab_GenInfo = QWidget()

        self.addTab(self.tab_SceneInfo, "Scene")
        self.addTab(self.tab_JobInfo, "Job")
        self.addTab(self.tab_GenInfo, "General")

        # -------------------------------------------------------------------------------------------------------------

        # Setup File Drop Location
        self.fileDrop_Name = QLabel('Drop File Here\nor...\nClick Here')
        self.fileDrop_Name.setToolTip(self.fileDrop_Name.text())
        self.fileDrop_Name.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.fileDrop_Name.setWordWrap(True)

        layout_Frame = QVBoxLayout()
        layout_Frame.addWidget(self.fileDrop_Name)

        self.fileDropLabel = QLabel('Scene File:')
        self.fileDropBox = FileDrop(self)
        self.fileDropBox.setLayout(layout_Frame)
        self.fileDropBox.areaClicked.connect(self.dropClicked)
        self.fileDropBox.fileDropped.connect(self.fileDropped)

        layout_Drop = QVBoxLayout()
        layout_Drop.addWidget(self.fileDropLabel)
        layout_Drop.addWidget(self.fileDropBox)

        # Setup Scene Information Line Items
        self.info_Renderer = HLineItem('Render Engine', ['rman', 'vray'], inputtype='list')
        self.info_Proj = HLineItem('Project Path', 'X:\\', inputtype='dir')
        self.info_Prefix = HLineItem('Image Prefix', 'crazytown')
        self.info_Frange = HLineItem('Frame Range', '1-10')
        self.info_Camera = HLineItem('Camera', 'cam_010')
        self.info_FrameDir = HLineItem('Image Directory', 'X:\\', inputtype='dir')

        self.info_Proj.searchClicked.connect(self.setProjPath)
        self.info_FrameDir.searchClicked.connect(self.setImagePath)

        sceneitems = [self.info_Renderer, self.info_Proj, self.info_Prefix, self.info_Frange, self.info_Camera, self.info_FrameDir]
        scenelist = HLineList(sceneitems)

        horizLine = HorizLine()

        self.line_Parse = HLineItem('Extract from File', 'Run', inputtype='btn')
        self.line_Parse.btn.pressed.connect(self.updateSceneVariables)

        # Setup Scene Tab Layout
        layout_Scene = QVBoxLayout()
        layout_Scene.addLayout(layout_Drop)
        layout_Scene.addLayout(scenelist)
        layout_Scene.addLayout(horizLine)
        layout_Scene.addLayout(self.line_Parse)
        self.tab_SceneInfo.setLayout(layout_Scene)

        # -------------------------------------------------------------------------------------------------------------

        self.info_Inst = HLineItem('# of Computers', '1', inputtype='int')
        self.info_Chunks = HLineItem('# of Chunks', '5', inputtype='int')
        self.info_Procs = HLineItem('Cores per Chunk', '10', inputtype='int')
        # info_Reservations = HLineItem('Reservations', 'host.processors=10')

        itemlist = [self.info_Inst, self.info_Chunks, self.info_Procs]
        linelist = HLineList(itemlist)

        self.list_incl = ListDrop(self)
        self.list_incl.itemDropped.connect(self.addInclItem)

        self.list_excl = ListDrop(self)
        self.list_excl.itemDropped.connect(self.addExclItem)

        layout_Job = QVBoxLayout()
        layout_Job.addLayout(linelist)

        layout_Job.addWidget(self.list_incl)
        layout_Job.addWidget(self.list_excl)


        self.tab_JobInfo.setLayout(layout_Job)

        # -------------------------------------------------------------------------------------------------------------

        self.info_Priority = HLineItem('Priority', '9999', inputtype='int')
        self.info_Prototype = HLineItem('Prototype', 'cmdrange')

        self.info_MayaExe = HLineItem('Executable', 'C:/Program Files/Autodesk/Maya2016.5/bin/Render.exe')
        self.info_Padding = HLineItem('Padding', '4', inputtype='int')

        genitems = [self.info_Priority, self.info_Prototype, self.info_MayaExe, self.info_Padding]
        genList = HLineList(genitems)

        layout_Gen = QVBoxLayout()
        layout_Gen.addLayout(genList)

        self.tab_GenInfo.setLayout(layout_Gen)

        # -------------------------------------------------------------------------------------------------------------

    def addInclItem(self, worker):
        item = QListWidgetItem(worker, self.list_incl)
        item.setStatusTip(worker)
        print self.list_excl.iterAllItems()

    def addExclItem(self, worker):
        item = QListWidgetItem(worker, self.list_excl)
        item.setStatusTip(worker)

    def setProjPath(self, b):
        if b is True:
            folderpath = self.getFolderPath('Set Project Folder')
            if folderpath is not None:
                self.info_Proj.input.setText(folderpath)
                self.info_Proj.input.setToolTip(self.info_Proj.input.text())
            else:
                self.logStatus.emit('No Project Folder Selected')

    def setImagePath(self, b):
        projpath = self.info_Proj.input.text()
        root = 'X:\\'
        startpath = root

        if projpath != root:
            startpath = projpath

        if b is True:
            folderpath = self.getFolderPath('Set Images Folder', basepath=startpath)
            if folderpath is not None:
                self.info_FrameDir.input.setText(folderpath)
                self.info_FrameDir.input.setToolTip(self.info_FrameDir.input.text())
            else:
                self.logStatus.emit('No Image Folder Selected')

    def dropClicked(self, b):
        projpath = self.info_Proj.input.text()
        root = 'X:\\'
        startpath = root

        if projpath != root:
            startpath = projpath

        if b is True:
            filepath = self.getFilePath('Set Maya Scene File', basepath=startpath)
            if filepath is not None:
                self.fileDrop_Name.setText(filepath)
                self.fileDrop_Name.setToolTip(self.fileDrop_Name.text())
            else:
                self.logStatus.emit('No Maya File Selected')

    def getFilePath(self, title, basepath='X:\\'):
        fileName = QFileDialog.getOpenFileName(self,
                                               str(title), basepath,
                                               str("Maya Files (*.ma *.mb)"))
        if fileName[0] != '':
            print(fileName)
            return fileName[0]
        else:
            print('Operation Canceled')
            return None

    def getFolderPath(self, title, basepath = 'X:\\'):
        fileName = QFileDialog.getExistingDirectory(self, str(title), basepath)
        if fileName != '':
            print(fileName)
            return fileName
        else:
            print('Operation Canceled')
            return None

    def fileDropped(self, l):
        for url in l:
            if os.path.exists(url):
                self.fileDrop_Name.setText(url)

    def updateSceneVariables(self):
        if os.path.exists(self.fileDrop_Name.text()):
            self.logStatus.emit('Parsing . . .')
            url = self.fileDrop_Name.text()
            data = parseMayaFile(url)

            cam = data[0]
            prefix = data[1]
            frames = data[2]

            self.info_Prefix.input.setText(prefix)
            self.info_Camera.input.setText(cam)
            self.info_Frange.input.setText(frames)
        self.logStatus.emit('Ready')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.main_widget = QWidget(self)

        self.layout_Tabs = TabLayout(self)
        self.layout_Tabs.logStatus.connect(self.setStatusBar)

        self.initUI()

    def initUI(self):

        self.statusBar().showMessage('Ready')

        main_layout = QHBoxLayout(self.main_widget)

        # -------------------------------------------------------------------------------------------------------------

        left_layout = QVBoxLayout()

        self.info_Name = HLineItem('Job Name', 'Qube Python Submission')
        self.btn_Submit = QPushButton('Submit Job')
        self.btn_Submit.setFixedHeight(50)
        self.btn_Submit.pressed.connect(self.submitJob)

        left_layout.addLayout(self.info_Name)
        left_layout.addWidget(self.layout_Tabs)
        left_layout.addWidget(self.btn_Submit)

        # -------------------------------------------------------------------------------------------------------------

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        workers = getWorkers()
        self.keys = ['Name', 'Address', 'State']
        self.worker_table = HTable(workers, self.keys)

        title_table = QLabel('All Workers')
        btn_refresh = QPushButton('Refresh')

        title_layout = QHBoxLayout()
        title_layout.addWidget(title_table)
        title_layout.addWidget(btn_refresh)

        btn_refresh.pressed.connect(self.refresh)

        right_layout.addLayout(title_layout)
        right_layout.addWidget(self.worker_table)

        # -------------------------------------------------------------------------------------------------------------

        vLine = VertLine()

        main_layout.addLayout(left_layout)
        main_layout.addLayout(vLine)
        main_layout.addLayout(right_layout)

        self.setCentralWidget(self.main_widget)
        self.show()

    def refresh(self):
        workers = getWorkers()
        keys = ['Name', 'Address', 'State']
        self.worker_table.refresh(workers, keys)

    @Slot(str)
    def setStatusBar(self, text):
        self.statusBar().showMessage(str(text))

    def submitJob(self):
        data = self.layout_Tabs
        job = Job()

        job.name = str(self.info_Name.input.text())
        job.insts = data.info_Inst.spinbox.value()
        job.priority = data.info_Priority.spinbox.value()
        job.ren = str(data.info_Renderer.list.currentText())
        job.procs = data.info_Procs.spinbox.value()
        job.proj = str(data.info_Proj.input.text())
        job.scene = str(data.fileDrop_Name.text())
        job.imgdir = str(data.info_FrameDir.input.text())
        job.cam = str(data.info_Camera.input.text())
        job.frange = str(data.info_Frange.input.text())
        job.chunks = data.info_Chunks.spinbox.value()

        job.setupPackage()
        print(job.qjob)

        QubeSubmit = Submit()
        QubeSubmit.addJob(job.qjob)
        QubeSubmit.submit()


#
# MAIN RUN FUNCTIONS
#

def main():
    # Create the Qt Application
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.setWindowTitle('Qube Submit')

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
