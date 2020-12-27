# -*- coding: utf-8 -*-

# Hazırlayan : Rahman Yazgan (rahmanyazgan@gmail.com)
# Lisans : GPL v.3

import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from moduller.Ui_Vakitler import Ui_Dialog

class AylikVakitler(QtWidgets.QDialog, Ui_Dialog):
    veritabaniVarmi = None
    
    def __init__(self, veritabaniDosyasi):
        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)
        
        self.tableView.setCornerButtonEnabled(False)
        
        veritabaniDosyasi = QtCore.QFile(veritabaniDosyasi)
        self.indis = 0
        self.vakitleriGoster(veritabaniDosyasi)
        
    def vakitleriGoster(self, veritabaniDosyasi):
        if QtCore.QFile.exists(veritabaniDosyasi):
            if veritabaniDosyasi.size() >= 4096:
                if self.veritabaninaBaglan(veritabaniDosyasi.fileName()):
                    self.tabloModeliniOlustur()
                    try:
                        self.tabloyuDoldur()
                        self.exec_()
                        AylikVakitler.veritabaniVarmi = True
                    except:
                        QtWidgets.QMessageBox.information(self, "Bilgilendirme",
                                                      "Aylık namaz vakitleri veritabanı boş. " + 
                                                      "\"Kapat\" butonuna bastığınızda veritabanınız güncellenecek.", 
                                                      "Kapat")
                        AylikVakitler.veritabaniVarmi = False
        else:
            AylikVakitler.veritabaniVarmi = False
            
    def tabloModeliniOlustur(self):
        self.satirSayisi = 30
        self.sutunSayisi = 8
        self.model = QtGui.QStandardItemModel(self.satirSayisi, self.sutunSayisi)
        
        sutunAdlari = ["Lokasyon", "Tarih", "İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"]
        
        self.indis = 0
        for sutunAdi in sutunAdlari:
            self.model.setHorizontalHeaderItem(self.indis, QtGui.QStandardItem(sutunAdi))
            self.indis = self.indis + 1
            
        self.tableView.setModel(self.model)
    
    def veritabaninaBaglan(self, veritabaniDosyasi):
        try:
            baglanti = sqlite3.connect(veritabaniDosyasi)
            self.imlec = baglanti.cursor()
            return True
        except sqlite3.OperationalError:
            print("Veritabanı yok.")
            AylikVakitler.veritabaniVarmi = False
            return False
    
    def veritabanindakiTumBilgileriCek(self):
        self.imlec.execute('SELECT * FROM namazvakitleri')
        veriler = self.imlec.fetchall()
        return veriler
    
    def tabloyuDoldur(self):
        veriler = self.veritabanindakiTumBilgileriCek()
                    
        for satir in range(0, self.satirSayisi, 1):
            for sutun in range(0, self.sutunSayisi, 1):                            
                nesne = QtGui.QStandardItem(veriler[satir][sutun])
                self.model.setItem(satir, sutun, nesne)
                
        self.imlec.close()