import os, sys
import qb

from PySide.QtCore import *
from PySide.QtGui import *

hosts = qb.hostinfo()
for host in hosts:
    name = host['name']
    address = host['address']
    status = host['state']
    string = '%s | %s | Status: %s' % (name, address, status)
    print string
    print host['resources']
    print "---"

title = ['name', 'address', 'state']


class HTable(QWidget):
    def __init__(self, parent=None):
        super(HTable, self).__init__(parent)

        colcnt = 3
        rowcnt = 8
        self.tablewidget = QTableWidget(rowcnt, colcnt)

        vheader = QHeaderView(Qt.Orientation.Vertical)
        vheader.setResizeMode(QHeaderView.ResizeToContents)
        self.tablewidget.setVerticalHeader(vheader)
        self.tablewidget.verticalHeader().hide()

        hheader = QHeaderView(Qt.Orientation.Horizontal)
        hheader.setResizeMode(QHeaderView.ResizeToContents)
        self.tablewidget.setHorizontalHeader(hheader)
        self.tablewidget.setHorizontalHeaderLabels(title)

        rowindex = 0
        colindex = 0
        for host in hosts:
            while colindex < colcnt:
                item = QTableWidgetItem(str(host[title[colindex]]))
                self.tablewidget.setItem(rowindex, colindex, item)
                colindex += 1
            colindex = 0
            rowindex += 1

        layout = QHBoxLayout()
        layout.addWidget(self.tablewidget)
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    widget = HTable()
    widget.show()
    widget.raise_()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()