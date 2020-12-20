#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hazırlayan : Rahman Yazgan (rahmanyazgan@gmail.com)
# Lisans : GPL v.3
# Sürüm : 1.62
# Platform : Windows

import sys
from PyQt4 import QtCore, QtGui
from moduller.PyVakitci import PyVakitci

class Program:
    version = 1.64
    
    def __init__(self):
        self.ayarlarKonum = QtCore.QDir.homePath() + "/.PyVakitci-" + str(self.version)
        self.ayarDosyasi = self.ayarlarKonum + "/ayarlar.ini"
        self.settings = QtCore.QSettings(self.ayarDosyasi, QtCore.QSettings.IniFormat)
        
        self.baslat()
        
    def baslat(self):
        self.pyvakitci = PyVakitci()

        if not self.pyvakitci.sistem_tepsisinde_baslat_checkBox.isChecked():
            self.pyvakitci.show()
        
        if self.pyvakitci.besmele_ile_basla_checkBox.isChecked():
            self.pyvakitci.besmeleyleBasla()
            
        self.zamanlayiciyiBaslat()
    
    def zamanlayiciyiBaslat(self):
        # Program uzun süre açık kaldığında ses dosyaları çalmadığından
        # dolayı 1 saatte bir program tekrar açılıyor.
        self.programTimer = QtCore.QTimer()
        self.programTimer.timeout.connect(self.programiCalistir)
        self.programTimer.start(3600000) # 3600000 ms = 1 saat
        
    def programiCalistir(self):
        self.saatleriAl()
        
        if self.saat in self.saatler.values():
            return
        else:
            self.pyvakitci.deleteLater()
            self.pyvakitci = PyVakitci()
            
    def saatleriAl(self):
        self.saat = QtCore.QTime().currentTime().toString("hh:mm")
        
        self.saatler = {}
        self.saatler["imsak"] = self.settings.value("Vakitler/imsak")
        self.saatler["gunes"] = self.settings.value("Vakitler/gunes")
        self.saatler["ogle"] = self.settings.value("Vakitler/ogle")
        self.saatler["ikindi"] = self.settings.value("Vakitler/ikindi")
        self.saatler["aksam"] = self.settings.value("Vakitler/aksam")
        self.saatler["yatsi"] = self.settings.value("Vakitler/yatsi")
        self.saatler["sela"] = self.settings.value("Vakitler/sela")
            
if __name__ == "__main__":
    # Uygulamanın tekrar açılmasını önlemeye yarayan yöntemlerden biri.
    sharedMemory = QtCore.QSharedMemory("a0bde891-444c-4ffe-99bb-117c4de5dc70")

    if(sharedMemory.create(512, QtCore.QSharedMemory.ReadWrite) == False):
        print("Uygulama zaten çalışıyor.")
        
        sys.exit(0)
    
    uygulama = QtGui.QApplication(sys.argv)
    program = Program()
    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    sys.exit(uygulama.exec_())
