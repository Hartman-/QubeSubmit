#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *

from internal import Job, Submit, getFrameRange, returnCamera

#
# GUI CLASSES
#

# Custom Line Item for information View
class HLineItem(QHBoxLayout):
    def __init__(self, labeltext='This is a longer title', inputtext='PLACEHOLDER', usenum=False, parent=None):
        super(HLineItem, self).__init__(parent)

        self.label = QLabel()
        self.label.setText(labeltext)
        self.label.setFixedWidth(125)
        self.label.setContentsMargins(0, 0, 40, 0)
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.input = QLineEdit()
        self.input.setText(inputtext)

        self.addWidget(self.label)

        if usenum is True and type(int(inputtext)) is int:
            self.spinbox = QSpinBox()
            self.spinbox.setRange(0, 9999)
            self.spinbox.setSingleStep(1)
            self.spinbox.setValue(int(inputtext))

            self.addWidget(self.spinbox)
        else:
            self.addWidget(self.input)

    def setInput(self, text):
        self.input.setText(str(text))

    def setLabel(self, text):
        self.label.setText(str(text))

    def getInputText(self):
        return self.input.text()

    def getInputValue(self):
        return self.spinbox.value()


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


class SubLayout(QTabWidget):
    def __init__(self, parent=None):
        super(SubLayout, self).__init__(parent)

        self.tab_JobInfo = QWidget()
        self.tab_SceneInfo = QWidget()
        self.tab_GenInfo = QWidget()

        self.addTab(self.tab_SceneInfo, "Scene")
        self.addTab(self.tab_JobInfo, "Job")
        self.addTab(self.tab_GenInfo, "General")

        # -------------------------------------------------------------------------------------------------------------

        info_Name = HLineItem('Job Name', 'Qube Python Submission')
        info_Inst = HLineItem('# of Computers', '1', usenum=True)
        info_Chunks = HLineItem('# of Chunks', '5', usenum=True)
        info_Procs = HLineItem('# of Cores / Chunk', '10', usenum=True)
        # info_Reservations = HLineItem('Reservations', 'host.processors=10')

        itemlist = [info_Name, info_Inst, info_Chunks, info_Procs]
        linelist = HLineList(itemlist)

        layout_Job = QVBoxLayout()
        layout_Job.addLayout(linelist)

        self.tab_JobInfo.setLayout(layout_Job)

        # -------------------------------------------------------------------------------------------------------------

        # Setup File Drop Location
        self.fileDrop_Name = QLabel('File Name...')
        self.fileDrop_Name.setWordWrap(True)
        layout_Frame = QVBoxLayout()
        layout_Frame.addWidget(self.fileDrop_Name)

        self.fileDropLabel = QLabel('Scene File:')
        self.fileDropBox = FileDrop(self)
        self.fileDropBox.setLayout(layout_Frame)
        self.fileDropBox.fileDropped.connect(self.fileDropped)

        layout_Drop = QVBoxLayout()
        layout_Drop.addWidget(self.fileDropLabel)
        layout_Drop.addWidget(self.fileDropBox)

        # Setup Scene Information Line Items
        info_Proj = HLineItem('Project Path', 'C:\\Users\\imh29')
        info_Frange = HLineItem('Frame Range', '1-10')
        info_Camera = HLineItem('Camera', 'cam_010')
        info_FrameDir = HLineItem('Image Directory', 'C:\\Users\\imh29')

        sceneitems = [info_Proj, info_Frange, info_Camera, info_FrameDir]
        scenelist = HLineList(sceneitems)

        btn_Parse = QPushButton('Parse Maya File')

        # Setup Scene Tab Layout
        layout_Scene = QVBoxLayout()
        layout_Scene.addLayout(layout_Drop)
        layout_Scene.addLayout(scenelist)
        layout_Scene.addWidget(btn_Parse)
        self.tab_SceneInfo.setLayout(layout_Scene)

        # -------------------------------------------------------------------------------------------------------------

        info_Priority = HLineItem('Priority', '9999', usenum=True)
        info_Prototype = HLineItem('Prototype', 'cmdrange')
        info_Renderer = HLineItem('Renderer', 'rman')
        info_MayaExe = HLineItem('Executable', 'C:/Program Files/Autodesk/Maya2016.5/bin/Render.exe')
        info_Padding = HLineItem('Padding', '4', usenum=True)

        genitems = [info_Priority, info_Prototype, info_Renderer, info_MayaExe, info_Padding]
        genList = HLineList(genitems)

        layout_Gen = QVBoxLayout()
        layout_Gen.addLayout(genList)

        self.tab_GenInfo.setLayout(layout_Gen)

        # -------------------------------------------------------------------------------------------------------------

    def fileDropped(self, l):
        for url in l:
            if os.path.exists(url):
                print(url)
                getFrameRange(url)
                self.fileDrop_Name.setText(url)
                # item = QListWidgetItem(url, self.fileDropBox)
                # item.setStatusTip(url)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainlayout = SubLayout()
        self.initUI()

    def initUI(self):

        self.setCentralWidget(self.mainlayout)
        self.setFixedWidth(300)
        self.show()


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
