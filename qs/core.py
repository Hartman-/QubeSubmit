#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os
import sys
import threading

from PySide.QtCore import *
from PySide.QtGui import *

from qs.internal import Job, Submit, parseMayaFile

#
# GUI CLASSES
#


class HorizLine(QHBoxLayout):
    def __init__(self, parent=None):
        super(HorizLine, self).__init__(parent)

        line = QFrame()
        line.setFrameStyle(QFrame.HLine | QFrame.Plain)
        line.setLineWidth(1)
        line.setStyleSheet("color: #777")

        self.addWidget(line)
        self.setContentsMargins(10, 20, 10, 20)


# Custom Line Item for information View
class HLineItem(QHBoxLayout):

    searchClicked = Signal(bool)

    def __init__(self, labeltext='PLACEHOLDER', inputtext='PLACEHOLDER', inputtype='string', parent=None):
        super(HLineItem, self).__init__(parent)

        self.label = QLabel()
        self.label.setText(labeltext)
        self.label.setFixedWidth(105)
        self.label.setContentsMargins(0, 0, 20, 0)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.addWidget(self.label)

        if inputtype == 'int' and type(int(inputtext)) is int:
            self.spinbox = QSpinBox()
            self.spinbox.setRange(0, 9999)
            self.spinbox.setSingleStep(1)
            self.spinbox.setValue(int(inputtext))

            self.addWidget(self.spinbox)

        elif inputtype == 'list' and type(inputtext) is list:
            self.list = QComboBox()

            for item in inputtext:
                self.list.addItem(item)

            self.addWidget(self.list)

        elif inputtype == 'btn' and type(inputtext) is str:
            self.btn = QPushButton(inputtext)
            self.addWidget(self.btn)

        elif inputtype == 'dir' and type(inputtext) is str:
            self.btn = QPushButton("...")
            self.btn.setFixedWidth(25)

            self.input = QLineEdit()
            self.input.setText(inputtext)
            self.input.setToolTip(inputtext)

            self.addWidget(self.input)
            self.addWidget(self.btn)

            self.btn.pressed.connect(self.emitClicked)

        else:
            self.input = QLineEdit()
            self.input.setText(inputtext)
            self.input.setToolTip(inputtext)
            self.addWidget(self.input)

    def emitClicked(self):
        self.searchClicked.emit(True)


class HLineList(QVBoxLayout):
    def __init__(self, itemlist, parent=None):
        super(HLineList, self).__init__(parent)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        for lineitem in itemlist:
            self.addLayout(lineitem)


class HTabLayout(QTabWidget):
    def __init__(self, parent=None):
        super(HTabLayout, self).__init__(parent)

        self.tab_JobInfo = QWidget()
        self.tab_GenInfo = QWidget()

        self.addTab(self.tab_JobInfo, "Job")
        self.addTab(self.tab_GenInfo, "General")


class FileDrop(QFrame):

    fileDropped = Signal(list)
    areaClicked = Signal(bool)

    def __init__(self, parent=None):
        super(FileDrop, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setFixedHeight(75)

        # Set Border
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLineWidth(1)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.fileDropped.emit(links)
        else:
            event.ignore()

    def mousePressEvent(self, event):
        self.areaClicked.emit(True)


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

        layout_Job = QVBoxLayout()
        layout_Job.addLayout(linelist)

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

    def setProjPath(self, b):
        if b is True:
            folderpath = self.getFolderPath('Set Project Folder')
            if folderpath is not None:
                self.info_Proj.input.setText(folderpath)
                self.info_Proj.input.setToolTip(self.info_Proj.input.text())
            else:
                self.logStatus.emit('No Project Folder Selected')

    def setImagePath(self, b):
        if b is True:
            folderpath = self.getFolderPath('Set Images Folder')
            if folderpath is not None:
                self.info_FrameDir.input.setText(folderpath)
                self.info_FrameDir.input.setToolTip(self.info_FrameDir.input.text())
            else:
                self.logStatus.emit('No Image Folder Selected')

    def dropClicked(self, b):
        if b is True:
            filepath = self.getFilePath('Set Maya Scene File')
            if filepath is not None:
                self.fileDrop_Name.setText(filepath)
                self.fileDrop_Name.setToolTip(self.fileDrop_Name.text())
            else:
                self.logStatus.emit('No Maya File Selected')

    def getFilePath(self, title):
        basePath = 'X:\\'
        fileName = QFileDialog.getOpenFileName(self,
                                               str(title), basePath,
                                               str("Maya Files (*.ma *.mb)"))
        if fileName[0] != '':
            print(fileName)
            return fileName[0]
        else:
            print('Operation Canceled')
            return None

    def getFolderPath(self, title):
        basePath = 'X:\\'
        fileName = QFileDialog.getExistingDirectory(self, str(title), basePath)
        if fileName != '':
            print(fileName)
            return fileName
        else:
            print('Operation Canceled')
            return None

    def fileDropped(self, l):
        for url in l:
            if os.path.exists(url):
                # print(url)
                # frames = getFrameRange(url)
                # self.info_Frange.input.setText(frames)
                self.fileDrop_Name.setText(url)

    def updateSceneVariables(self):
        # print(self.fileDrop_Name.text())
        if self.fileDrop_Name.text() != 'File Name...':
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

        main_layout = QVBoxLayout(self.main_widget)

        self.info_Name = HLineItem('Job Name', 'Qube Python Submission')
        self.btn_Submit = QPushButton('Submit Job')
        self.btn_Submit.pressed.connect(self.submitJob)

        main_layout.addLayout(self.info_Name)
        main_layout.addWidget(self.layout_Tabs)
        main_layout.addWidget(self.btn_Submit)
        self.setCentralWidget(self.main_widget)
        self.setFixedWidth(300)


        self.show()

    @Slot(str)
    def setStatusBar(self, text):
        self.statusBar().showMessage(str(text))

    def submitJob(self):
        data = self.layout_Tabs
        job = Job(
            self.info_Name.input.text(),
            data.info_Inst.spinbox.value(),
            data.info_Priority.spinbox.value(),
            data.info_Renderer.list.currentText(),
            data.info_Procs.spinbox.value(),
            data.info_Proj.input.text(),
            data.fileDrop_Name.text(),
            data.info_FrameDir.input.text(),
            data.info_Camera.input.text(),
            data.info_Frange.input.text(),
            data.info_Chunks.spinbox.value()
        )

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
