#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import random
import sys

import re

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


class VertLine(QVBoxLayout):
    def __init__(self, parent=None):
        super(VertLine, self).__init__(parent)

        line = QFrame()
        line.setFrameStyle(QFrame.VLine | QFrame.Plain)
        line.setLineWidth(1)
        line.setStyleSheet("color: #777")

        self.addWidget(line)
        self.setContentsMargins(20, 10, 20, 10)


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
        self.setFixedHeight(100)

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


class ListDrop(QListWidget):

    itemDropped = Signal(object)

    def __init__(self, parent=None):
        super(ListDrop, self).__init__(parent)
        self.setAcceptDrops(True)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # create context menu
        self.rightClickMenu = QMenu(self)
        self.act_Remove = QAction('Remove', self)
        self.rightClickMenu.addAction(self.act_Remove)
        self.act_Remove.triggered.connect(self.removeItem)
        # self.rightClickMenu.addAction(QAction('test1', self))
        # self.rightClickMenu.addSeparator()
        # self.rightClickMenu.addAction(QAction('test2', self))

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)

        data = event.mimeData()
        if data.formats()[0] == 'application/x-qabstractitemmodeldatalist':
            event.accept()

            # StackOverflow Wizard Magic Right Here
            model = QStandardItemModel()
            model.dropMimeData(data, Qt.CopyAction, 0,0, QModelIndex())

            uniText = model.item(0).text()
            # No Duplicates!
            if uniText not in self.iterAllItems():
                self.itemDropped.emit(uniText)

    def iterAllItems(self):
        list = []
        for i in range(self.count()):
            text = str(self.item(i).text())
            list.append(text)
        return list

    def on_context_menu(self, point):
        if self.itemAt(point) is not None:
            self.rightClickMenu.exec_(self.mapToGlobal(point))

    def removeItem(self):
        self.takeItem(self.row(self.selectedItems()[0]))


class HTable(QWidget):
    def __init__(self, hosts, keys, parent=None):
        super(HTable, self).__init__(parent)
        self.setAcceptDrops(True)

        self.hosts = hosts
        self.keys = keys

        self.colcnt = len(self.keys)
        self.rowcnt = len(self.hosts)

        self.tablewidget = QTableWidget(self.rowcnt, self.colcnt)
        self.tablewidget.setSortingEnabled(True)

        self.tablewidget.setAcceptDrops(True)
        self.tablewidget.setDragEnabled(True)

        self.initTable()

    def initTable(self):
        vheader = QHeaderView(Qt.Orientation.Vertical)
        # vheader.setResizeMode(QHeaderView.ResizeToContents)
        self.tablewidget.setVerticalHeader(vheader)
        self.tablewidget.verticalHeader().hide()

        hheader = QHeaderView(Qt.Orientation.Horizontal)
        # hheader.setResizeMode(QHeaderView.ResizeToContents)
        self.tablewidget.setHorizontalHeader(hheader)
        hheader.setClickable(True)
        self.tablewidget.setHorizontalHeaderLabels(self.keys)

        self.buildTable()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tablewidget)
        self.setLayout(layout)

    def buildTable(self):
        self.tablewidget.setSortingEnabled(False)

        dragFlags = Qt.ItemIsEnabled | Qt.ItemIsDragEnabled | Qt.ItemIsSelectable | Qt.ItemIsDropEnabled
        staticFlags = Qt.ItemIsEnabled

        rowindex = 0
        colindex = 0
        for host in self.hosts:
            while colindex < self.colcnt:
                item = QTableWidgetItem(str(host[self.keys[colindex].lower()]))
                if colindex == 0:
                    item.setFlags(dragFlags)
                else:
                    item.setFlags(staticFlags)
                self.tablewidget.setItem(rowindex, colindex, item)
                self.tablewidget.setColumnWidth(colindex, 100)
                colindex += 1
            colindex = 0
            rowindex += 1
        self.tablewidget.setSortingEnabled(True)

    def updateTableLayout(self, keys):
        self.keys = keys
        self.colcnt = len(self.keys)
        self.rowcnt = len(self.hosts)

        self.tablewidget.setColumnCount(self.colcnt)
        self.tablewidget.setRowCount(self.rowcnt)

        self.tablewidget.setHorizontalHeaderLabels(self.keys)

    def refresh(self, hosts, newkeys):
        self.hosts = hosts

        # Check if Keys/Titles changed
        if len(newkeys) > len(self.keys):
            self.updateTableLayout(newkeys)
        else:
            # If the order changes, update the columns
            for i, key in enumerate(newkeys):
                if key != self.keys[i]:
                    self.updateTableLayout(newkeys)

        # Update the table info regardless
        # Allows for information to update even if keys/titles haven't changed
        self.buildTable()