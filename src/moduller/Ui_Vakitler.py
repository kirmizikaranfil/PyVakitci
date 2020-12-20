# -*- coding: utf-8 -*-

# Created: Tue Oct 22 23:02:26 2013
#      by: PyQt4 UI code generator 4.10.3

from PyQt4 import QtCore, QtGui

try:
    def _fromUtf8(s):
        return s
except:
    _fromUtf8 = QtCore.QString.fromUtf8

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(805, 550)
        Dialog.setMinimumSize(QtCore.QSize(805, 550))
        Dialog.setMaximumSize(QtCore.QSize(805, 550))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        Dialog.setFont(font)
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 805, 552))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tableView = QtGui.QTableView(self.horizontalLayoutWidget)
        self.tableView.setMinimumSize(QtCore.QSize(805, 550))
        self.tableView.setMaximumSize(QtCore.QSize(805, 550))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.tableView.setFont(font)
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.horizontalHeader().setDefaultSectionSize(85)
        self.tableView.horizontalHeader().setMinimumSectionSize(85)
        self.horizontalLayout.addWidget(self.tableView)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Aylık Vakitler (diyanet.gov.tr)", None))

