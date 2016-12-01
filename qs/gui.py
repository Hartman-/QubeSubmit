#!/usr/bin/python
# -'''- coding: utf-8 -'''-

from PySide.QtCore import *
from PySide.QtGui import *


class HorizLine(QHBoxLayout):
    def __init__(self, parent=None):
        super(HorizLine, self).__init__(parent)

        line = QFrame()
        line.setFrameStyle(QFrame.HLine | QFrame.Plain)
        line.setLineWidth(1)
        line.setStyleSheet("color: #777")

        self.addWidget(line)
        self.setContentsMargins(10, 20, 10, 20)


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