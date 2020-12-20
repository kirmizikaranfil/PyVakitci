# -*- coding: utf-8 -*-

# Hazırlayan : Rahman Yazgan (rahmanyazgan@gmail.com)
# Lisans : GPL v.3

from PyQt4 import QtGui, QtCore
from moduller.Ui_Hakkinda import Ui_Dialog

class Hakkinda(QtGui.QDialog, Ui_Dialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        
        self.hakkinda_label.linkActivated.connect(self.siteyeGir)
        self.yazar_label.linkActivated.connect(self.siteyeGir)
        self.hata_bildirimi_label.linkActivated.connect(self.siteyeGir)
    
    def siteyeGir(self, URL):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(URL))
