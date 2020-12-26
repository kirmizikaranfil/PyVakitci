#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Hazırlayan : Rahman Yazgan (rahmanyazgan@gmail.com)
# Lisans : GPL v.3
# Sürüm : 1.7
# Platform : Windows

import datetime, os, platform, re, shutil, sys, threading, urllib.request, webbrowser, winreg

try:
    from PyQt4 import QtCore, QtGui
    from PyQt4.phonon import Phonon
except:
    url = "http://www.riverbankcomputing.co.uk/software/pyqt/download"
    print("PyQt4 modülü ve/veya Phonon yüklü değil.\n\n" +
          "Kurulum:\n" + url + "\n\n" +
          "sitesine giderek sisteminizdeki kurulu Python sürümüne uygun olanı indiriniz.\n" +
          "Yükledikten sonra PyVakitci'yi çalıştırmayı tekrar deneyebilirsiniz.\n\n")

    siteyeGit = input("PyQt4 modülünü indirmek için 1 yazın: ")

    if siteyeGit == "1":
        webbrowser.open_new_tab(url)

    exit()
   
from moduller.DiyanetUlkeler import DiyanetUlkeler
from moduller.SehirleriAl import SehirleriAl
from moduller.IlceleriAl import IlceleriAl

from moduller.SiteyeBaglan import SiteyeBaglan
from moduller.Vakitler import Vakitler

from moduller.Calverter import Calverter
from moduller.Clever import Clever

from moduller.AylikVakitler import AylikVakitler
from moduller.Ui_PyVakitci import Ui_MainWindow

class PyVakitci(QtGui.QMainWindow, Ui_MainWindow):
    calismaDizini = ""
    diyanetUlkeler = None
    ilceler = None
    sehirler = None
    rlock = None
    veritabaniDosyasi = None
    version = 1.7

    def __init__(self):
        super(PyVakitci, self).__init__()
        self.setupUi(self)
        
        self.phononModulunuAktiflestir()
        self.degiskenleriHazirla()
        self.sinyalleriEkle()
        self.cleanlooksGorunumu()
        self.calismaDizininiHazirla()
        self.bolgeselAyarlar()
        self.ekrandaOrtala()
        self.sesVarsayilanAyarlar()
        self.ayarlariUygula()
        self.trayIconGoster()
        self.hicriTarihiGuncelle()
        self.otomatikGuncellestir()
        self.saatGuncelleyiciyiCalistir()
       
    def phononModulunuAktiflestir(self):
        self.mediaNesnesi = Phonon.MediaObject(self)
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.mediaNesnesi, self.audioOutput)

        self.volumeSlider.setAudioOutput(self.audioOutput)
           
    def degiskenleriHazirla(self):        
        self.volume = 0

        self.programinKonumu = os.getcwd().replace(os.sep, "/")
        self.sesDosyalariKonum = self.programinKonumu + "/ses_dosyalari/"
        self.tempPath = QtCore.QDir.tempPath()
        self.ayarlarKonum = QtCore.QDir.homePath() + "/.PyVakitci-" + str(self.version)
        self.ayarDosyasi = self.ayarlarKonum + "/ayarlar.ini"
       
        self.diyanetURL = DiyanetUlkeler.BASE_URL
       
        SehirleriAl.ayarDosyasi = self.ayarDosyasi
        IlceleriAl.ayarDosyasi = self.ayarDosyasi
       
        self.ontanimliAyarDosyasi = self.programinKonumu + "/ontanimli_ayarlar.ini"
       
        self.settings = QtCore.QSettings(self.ayarDosyasi, QtCore.QSettings.IniFormat)
        self.settingsVarsayilan = QtCore.QSettings(self.ontanimliAyarDosyasi, QtCore.QSettings.IniFormat)
       
        PyVakitci.diyanetUlkeler = DiyanetUlkeler()
        self.winampKontrol = Clever(self.programinKonumu)
       
        self.lisansDosyasi = str(self.programinKonumu + "/GPLv3_TR.html")
        self.besmeleDosyasi = self.sesDosyalariKonum + "besmele.mp3"

        self.simdikiTarih = QtCore.QDate().currentDate().toString("dd MMMM yyyy")
        Vakitler.simdikiTarih = QtCore.QDate().currentDate().toString("dd.MM.yyyy")

        self.diniGunlerVeGeceler = ["11 Rebiülevvel", "1 Recep", "6 Recep", "26 Recep", "14 Şaban",
                                    "1 Ramazan", "27 Ramazan", "30 Ramazan", "1 Şevval", "2 Şevval",
                                    "3 Şevval", "9 Zilhicce", "10 Zilhicce", "11 Zilhicce",
                                    "12 Zilhicce", "13 Zilhicce", "1 Muharrem", "10 Muharrem"]

        self.diniGunlerVeGecelerKarsiligi = ["Mevlid Kandili", "Üç Aylar'ın Başlangıcı", "Regaib Kandili",
                                             "Miraç Kandili", "Beraat Kandili", "Ramazan'ın Başlangıcı",
                                             "Kadir Gecesi", "Arefe","Ramazan Bayramı (1. gün)", "Ramazan Bayramı (2. gün)",
                                             "Ramazan Bayramı (3. gün)", "Arefe", "Kurban Bayramı (1. gün)",
                                             "Kurban Bayramı (2. gün)", "Kurban Bayramı (3. gün)",
                                             "Kurban Bayramı (4. gün)", "Hicri Yılbaşı", "Aşure Günü"]

        self.mesajGosterildi = False
        self.diniGunMesajiGosterildi = False

        self.windowFlag = None

        self.rlock = threading.RLock()

    def sinyalleriEkle(self):
        self.actionCleanlooks.triggered.connect(self.cleanlooksGorunumu)
        self.actionPlastique.triggered.connect(self.plastiqueGorunumu)
        self.actionWindowsXP.triggered.connect(self.windowsXPGorunumu)
        self.actionWindowsVista.triggered.connect(self.windowsVistaGorunumu)
        self.actionCikis.triggered.connect(self.programiKapat)
        self.actionVakitleriGoster.triggered.connect(self.vakitleriGoster)
        self.actionLisans.triggered.connect(self.lisans)
        self.actionHakkinda.triggered.connect(self.hakkindaDialog)
        self.actionQtHakkinda.triggered.connect(QtGui.QApplication.aboutQt)
        self.ikon_goster_checkBox.stateChanged.connect(self.trayIconGoster)
        self.her_zaman_ustte_checkBox.stateChanged.connect(self.herZamanUstte)
        self.winamp_duraklat_checkBox.stateChanged.connect(self.winampVarMi)
        self.audioOutput.mutedChanged.connect(self.sesAyari)
        self.audioOutput.volumeChanged.connect(self.mutedAyari)
        self.sabah_ezani_oku_checkBox.stateChanged.connect(self.ezanOkuKontrol)
        self.ogle_ezani_oku_checkBox.stateChanged.connect(self.ezanOkuKontrol)
        self.ikindi_ezani_oku_checkBox.stateChanged.connect(self.ezanOkuKontrol)
        self.aksam_ezani_oku_checkBox.stateChanged.connect(self.ezanOkuKontrol)
        self.yatsi_ezani_oku_checkBox.stateChanged.connect(self.ezanOkuKontrol)
        self.erken_uyari_checkBox.stateChanged.connect(self.erkenUyari)
        self.vakitleri_guncelle_pushButton.clicked.connect(self.diyanetAylikVakitleriKaydet)
        self.vakitleri_goster_pushButton.clicked.connect(self.vakitleriTopluGoster)
        self.bolgesel_ayarlar_kaydet_pushButton.clicked.connect(self.ayarlariKaydet)
        self.bolgesel_ayarlar_varsayilan_pushButton.clicked.connect(self.varsayilanAyarlar)
        self.ayarlar_kaydet_pushButton.clicked.connect(self.ayarlariKaydet)
        self.ayarlar_varsayilan_pushButton.clicked.connect(self.varsayilanAyarlar)
        self.sabah_toolButton.clicked.connect(self.sesDosyasiEkleSabah)
        self.ogle_toolButton.clicked.connect(self.sesDosyasiEkleOgle)
        self.ikindi_toolButton.clicked.connect(self.sesDosyasiEkleIkindi)
        self.aksam_toolButton.clicked.connect(self.sesDosyasiEkleAksam)
        self.yatsi_toolButton.clicked.connect(self.sesDosyasiEkleYatsi)
        self.dua_toolButton.clicked.connect(self.sesDosyasiEkleDua)
        self.sela_toolButton.clicked.connect(self.sesDosyasiEkleSela)
        self.uyari_toolButton.clicked.connect(self.sesDosyasiEkleUyari)
        self.ses_kaydet_pushButton.clicked.connect(self.ayarlariKaydet)
        self.ses_varsayilan_pushButton.clicked.connect(self.sesVarsayilanAyarlar)
        self.trayIcon.activated.connect(self.iconActivated)
        self.pushButton_android.clicked.connect(self.risaleAppForAndroid)
        self.pushButton_ios.clicked.connect(self.risaleAppForIOS)
        
    def risaleAppForAndroid(self):
        url = "https://play.google.com/store/apps/details?id=com.nesil.risalei_nur&hl=tr&gl=US"
        self.siteAc(url)
        
    def risaleAppForIOS(self):
        url = "https://apps.apple.com/az/app/risale-i-nur-k%C3%BClliyat%C4%B1-s%C3%B6z/id814437480"
        self.siteAc(url)
        
    def trayIconGoster(self):
        if self.ikon_goster_checkBox.isChecked():
            if not self.trayIcon.isVisible():
                self.trayIcon.show()
            else:
                self.hide()
                
            if self.sistem_tepsisinde_baslat_checkBox.isChecked():
                self.hide()
            else:
                self.show()
                
            self.sistem_tepsisinde_baslat_checkBox.setEnabled(True)
        else:
            self.sistem_tepsisinde_baslat_checkBox.setEnabled(False)
            self.sistem_tepsisinde_baslat_checkBox.setChecked(False)
            self.trayIcon.hide()
            self.show()

    def ekrandaOrtala(self):
        self.move((QtGui.QDesktopWidget().screenGeometry().width() - self.geometry().width()) / 2,
                  (QtGui.QDesktopWidget().screenGeometry().height() - self.geometry().height()) / 2)

    def calismaDizininiHazirla(self):
        if QtCore.QDir.exists(QtCore.QDir(self.ayarlarKonum)) == False:
            QtCore.QDir(QtCore.QDir.homePath()).mkpath(".PyVakitci-" + str(self.version))

        self.calismaDizini = self.ayarlarKonum
        PyVakitci.veritabaniDosyasi = str(self.calismaDizini + "/diyanet.db")
       
    def varsayilanAyarlariKopyala(self):
        self.ontanimliAyarDosyasiYeni = self.tempPath + "/ontanimli_ayarlar.ini"
       
        if not (QtCore.QFile.exists(QtCore.QFile(self.ontanimliAyarDosyasiYeni))):
            shutil.copy(self.ontanimliAyarDosyasi, self.ontanimliAyarDosyasiYeni)
           
        self.ontanimliAyarDosyasi = self.ontanimliAyarDosyasiYeni
        
    def mesajKutusunuGoster(self, surumNotlari, version):
        messageBox = QtGui.QMessageBox()
        ikon = QtGui.QIcon()
        ikon.addPixmap(QtGui.QPixmap(":resimler/cami.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        messageBox.setWindowIcon(ikon)
        messageBox.setIcon(QtGui.QMessageBox.Question)
        messageBox.setWindowTitle("Güncelleme")
        
        yesButton = QtGui.QPushButton('Yeni Kurulum (23 mb)')
        noButton = QtGui.QPushButton('Güncelleme (2 mb)')
        cancelCheckBox = QtGui.QCheckBox("Bir Daha Gösterme")
        
        messageBox.addButton(yesButton, QtGui.QMessageBox.YesRole)        
        messageBox.addButton(noButton, QtGui.QMessageBox.NoRole)
        messageBox.addButton(cancelCheckBox, QtGui.QMessageBox.RejectRole)
        messageBox.setDefaultButton(noButton)
        
        version = str(version)
        surumNotlari = str(surumNotlari)
        
        messageBox.setText("PyVakitci programının yeni sürümü mevcut.\n\n" +
                           "PyVakitci " + version + " sürümündeki yenilikler:\n\n" +
                           surumNotlari + "\n\n" +
                           "PyVakitci " + version + " sürümünü indirmek ister misiniz?")

        messageBox.exec_()
        
        if messageBox.clickedButton() == yesButton:
            url = "https://goo.gl/cPxj3s"
            self.siteAc(url)
        
        if messageBox.clickedButton() == noButton:
            url = "https://goo.gl/QBySgt"
            self.siteAc(url)
            
        if messageBox.clickedButton() == cancelCheckBox:
            self.otomatik_guncellestir_checkBox.setChecked(False)
            self.ayarlariKaydet()

    def otomatikGuncellestir(self):
        if self.otomatik_guncellestir_checkBox.isChecked():
            url = "https://sourceforge.net/projects/pyvakitci2011/files/"
            file_url = "https://master.dl.sourceforge.net/project/pyvakitci2011"
            
            if self.siteyeBaglantiVarMi(url):
                site = urllib.request.urlopen(file_url + "/Version")
                
                version = float(site.read())
                
                if self.version < version:
                    site = urllib.request.urlopen(file_url +"/SurumNotlari")
                        
                    surumNotlari = site.read().decode('utf-8')
                    
                    self.mesajKutusunuGoster(surumNotlari, version)

    # trayIcon a tıklandığında program görünür/görünmez olur.
    def iconActivated(self, reason):
        if reason in (QtGui.QSystemTrayIcon.Trigger, QtGui.QSystemTrayIcon.DoubleClick):
            try:
                if self.isVisible():
                    self.hide()
                else:
                    self.tabWidget.setCurrentIndex(0)
                    self.show()
            except AttributeError:
                pass

    def cleanlooksGorunumu(self):
        self.gorunumuDegistir("Cleanlooks")

    def plastiqueGorunumu(self):
        self.gorunumuDegistir("Plastique")

    def windowsXPGorunumu(self):
        self.gorunumuDegistir("WindowsXP")

    def windowsVistaGorunumu(self):
        self.gorunumuDegistir("WindowsVista")

    def gorunumuDegistir(self, lookAndFeel):
        self.gorunum = lookAndFeel
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(self.gorunum))

    # Visual Basic Script koduyla kısayol dosyası oluşturularak başlangıç dizinine ekleniyor.
    def vbScriptKodu(self, durum):
        if durum:
            kod = """
                    sub KisayolOlustur()
                      dim shell, baslangicDizini, kisayolDosyasi

                      set shell = CreateObject("WScript.Shell")
                      baslangicDizini = shell.SpecialFolders("Startup")
                      set kisayolDosyasi = shell.CreateShortcut(baslangicDizini + "\PyVakitci.lnk")
                      kisayolDosyasi.TargetPath = "%s\\Program.py"
                      kisayolDosyasi.WindowStyle = 1
                      kisayolDosyasi.WorkingDirectory = "%s\\"
                      kisayolDosyasi.Save
                    end sub

                    call KisayolOlustur()
                    """ %(self.programinKonumu, self.programinKonumu)
        else:
            kod = """
                sub DosyaSil()
                    dim kisayolDosyasi, objFSO, shell

                    Set shell = CreateObject("WScript.Shell")
                    kisayolDosyasi = shell.SpecialFolders("Startup") + "\PyVakitci.lnk"

                    Set objFSO = CreateObject("Scripting.FileSystemObject")
                    If objFSO.FileExists(kisayolDosyasi) Then
                        objFSO.DeleteFile(kisayolDosyasi)
                    End If

                end sub

                call DosyaSil()
                """
        return kod

    def otomatikCalistir(self):
        isletimSistemi = platform.system()
        windowsVersion = float(platform.version()[:3])
       
        if isletimSistemi == "Windows":
            if windowsVersion >= 6.0:
                if self.otomatik_calistir_checkBox.isChecked():
                    veriler = self.vbScriptKodu(True)
           
                if self.otomatik_calistir_checkBox.isChecked() == False:
                    veriler = self.vbScriptKodu(False)
           
                self.visualBasicScriptCalistir(veriler)
               
            if windowsVersion < 6.0:
                programinKonumu = (self.programinKonumu + "/Program.py").replace("/", os.sep)
                regYolu = "Software/Microsoft/Windows/CurrentVersion/Run".replace("/", os.sep)
                keyEx = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, regYolu, 0, winreg.KEY_ALL_ACCESS)
           
                if self.otomatik_calistir_checkBox.isChecked():
                    winreg.SetValueEx(keyEx, "PyVakitci", 0, winreg.REG_SZ, programinKonumu)
           
                if self.otomatik_calistir_checkBox.isChecked() == False:
                    try:
                        winreg.DeleteValue(keyEx, "PyVakitci")
                    except:
                        pass
                   
                winreg.CloseKey(keyEx)

    def visualBasicScriptCalistir(self, veriler):
        dosya = self.tempPath + "/pyvakitci.vbs"
        
        with open(dosya, 'w') as dosyaIslemi:
            dosyaIslemi.write(veriler)
            dosyaIslemi.close()
   
            if QtCore.QFile.exists(QtCore.QFile(dosya)):
                os.popen(str("wscript.exe " + dosya))
               
                from time import sleep
                sleep(2)
               
                QtCore.QFile(dosya).remove()

    def besmeleyleBasla(self):
        if self.besmele_ile_basla_checkBox.isChecked():
            self.sesDosyasiniAc(self.besmeleDosyasi)

    def herZamanUstte(self):
        if self.her_zaman_ustte_checkBox.isChecked():
            self.windowFlag = self.windowFlags()
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlag)
            self.windowFlag = None
        
        if not self.isVisible():
            self.show()

        self.ekrandaOrtala()

    def ezanOkuKontrol(self):
        if self.sabah_ezani_oku_checkBox.isChecked() or +\
            self.ogle_ezani_oku_checkBox.isChecked() or  +\
            self.ikindi_ezani_oku_checkBox.isChecked() or +\
            self.aksam_ezani_oku_checkBox.isChecked() or +\
            self.yatsi_ezani_oku_checkBox.isChecked():
           
            self.dua_oku_checkBox.setEnabled(True)
        else:
            self.dua_oku_checkBox.setEnabled(False)
            self.dua_oku_checkBox.setChecked(False)

    def erkenUyari(self):
        if self.erken_uyari_checkBox.isChecked():
            self.erken_uyari_spinBox.setEnabled(True)
            self.uyari_sesi_checkBox.setEnabled(True)
        else:
            self.erken_uyari_spinBox.setEnabled(False)
            self.uyari_sesi_checkBox.setEnabled(False)
            self.uyari_sesi_checkBox.setChecked(False)

    def karakterKontrol(self):
        QtGui.QMessageBox.warning(self, "Hata", "0 ve 99 arasında bir sayı girin.", "Tamam")

    def dosyaEkle(self, lineEdit):
        konum = QtGui.QFileDialog.getOpenFileName(self, "Aç", "", "Ses Dosyaları (*.mp3 *.ogg *.wma *.wav)")

        if len(konum) > 0:
            lineEdit.setText(konum)
           
    def winampVarMi(self):
        if self.winamp_duraklat_checkBox.isChecked():
            winampKonum = self.settings.value("Ayarlar/winamp_konum")
            
            if winampKonum == None:
                QtGui.QMessageBox.information(self, "Bilgilendirme",
                                              "Winamp programını seçmeniz gerekiyor. \nProgram seçerken aşağıdaki konumlara bakın:\n\n" +
                                              "C:\\Program Files\\Winamp\n" +
                                              "C:\\Program Files (x86)\\Winamp\n" +
                                              "C:\\Program Dosyaları (x86)\\Winamp\n" +
                                              "C:\\Program Dosyaları\\Winamp\n",
                                              "Tamam")
                konum = QtGui.QFileDialog.getOpenFileName(self, "Aç", "", "Exe Dosyaları (winamp.exe)")
       
                if len(konum) > 0:
                    self.settings.setValue("Ayarlar/winamp_konum", konum)
                    self.winamp_duraklat_checkBox.setChecked(True)
                    return True
                else:
                    self.winamp_duraklat_checkBox.setChecked(False)
                    return False

    def sesDosyasiEkleSabah(self):
        self.dosyaEkle(self.sabah_lineEdit)

    def sesDosyasiEkleOgle(self):
        self.dosyaEkle(self.ogle_lineEdit)

    def sesDosyasiEkleIkindi(self):
        self.dosyaEkle(self.ikindi_lineEdit)

    def sesDosyasiEkleAksam(self):
        self.dosyaEkle(self.aksam_lineEdit)

    def sesDosyasiEkleYatsi(self):
        self.dosyaEkle(self.yatsi_lineEdit)

    def sesDosyasiEkleDua(self):
        self.dosyaEkle(self.dua_lineEdit)
       
    def sesDosyasiEkleSela(self):
        self.dosyaEkle(self.sela_lineEdit)

    def sesDosyasiEkleUyari(self):
        self.dosyaEkle(self.uyari_lineEdit)

    def sesAyari(self):
        if self.volume == None:
            self.volume = self.audioOutput.volume()
            self.audioOutput.setVolume(0)
        else:
            self.audioOutput.setVolume(self.volume)
            self.volume = None

    def mutedAyari(self, volume):
        if volume == 0:
            self.audioOutput.setMuted(True)
        else:
            self.audioOutput.setMuted(False)
           
    def saatGuncelleyiciyiCalistir(self):
        self.timerSaat = QtCore.QTimer()
        self.timerSaat.timeout.connect(self.saatiGuncelle)
        self.timerSaat.start(600)

    def saatiGuncelle(self):
        self.saat = QtCore.QTime().currentTime().toString("hh:mm:ss")
        self.saat_label.setText("Saat: " + self.saat)

        self.tarih = QtCore.QDate().currentDate().toString("d MMMM yyyy")
        self.miladi_tarih.setText(self.tarih)

        if self.simdikiTarih != self.tarih:
            self.miladi_tarih.setText(self.tarih)
            self.simdikiTarih = self.tarih
            self.hicriTarihiGuncelle()
            self.vakitleriAl()

    def hicriTarihiBul(self):
        yil = int(QtCore.QDate().currentDate().toString("yyyy"))
        ay = int(QtCore.QDate().currentDate().toString("M"))
        gun = int(QtCore.QDate().currentDate().toString("d"))
       
        if self.hicri_gun_ekle_checkBox.isChecked():
            ilaveGun = int(self.hicri_tarih_gun_ekle_spinBox.text())
        else:
            ilaveGun = 0
       
        gun = gun + ilaveGun

        self.hicriAylar = ["Muharrem", "Safer", "Rebiülevvel", "Rebiülahir",
                           "Cemaziyelevvel", "Cemaziyelahir", "Receb", "Şaban",
                           "Ramazan", "Şevval", "Zilkade", "Zilhicce"]

        self.calverter = Calverter()
        jd = self.calverter.gregorian_to_jd(yil, ay, gun)
        hicri_tarih = self.calverter.jd_to_islamic(jd)

        self.hicriYil = str(hicri_tarih[0])
        self.hicriAy = str(self.hicriAylar[hicri_tarih[1] - 1])
        self.hicriGun = str(hicri_tarih[2])

        self.hicriTarih = self.hicriGun + " " + self.hicriAy + " " + self.hicriYil

    def hicriTarihiGuncelle(self):
        self.hicriTarihiBul()
        self.hicri_tarih.setText(self.hicriTarih)
        self.diniGunleriHatirlat()

    def diniGunleriHatirlat(self):
        hicriGunVeAy = str(self.hicriGun + " " + self.hicriAy)

        if self.diniGunlerVeGeceler.count(hicriGunVeAy) == 1:
            diniGun = str(self.diniGunlerVeGecelerKarsiligi[self.diniGunlerVeGeceler.index(hicriGunVeAy)])

            self.dini_gun_label.setText("<font color='#0174DF' size='3'>" + diniGun  + "</font>")

            if self.diniGunMesajiGosterildi == False:
                mesaj = hicriGunVeAy + " - " + diniGun
                self.mesajGoster("Dini Günler ve Geceler", "\n" + mesaj)
                self.diniGunMesajiGosterildi = True
        else:
            self.dini_gun_label.clear()

    def labelTemizlik(self):
        self.ulke_label.clear()
        self.sehir_label.clear()
        Vakitler.saatler = ""
        self.namaz_vakti_label.clear()
        self.imsak_saat_label.clear()
        self.gunes_saat_label.clear()
        self.ogle_saat_label.clear()
        self.ikindi_saat_label.clear()
        self.aksam_saat_label.clear()
        self.yatsi_saat_label.clear()
        self.sonraki_vakit_label.clear()
        self.kalan_sure_label.clear()

    def bolgeselAyarlar(self):
        self.labelTemizlik()
       
        self.ulkeler_comboBox.clear()
        self.sehirler_comboBox.clear()
       
        for ulke in sorted(self.diyanetUlkeler.ulkeler):
            self.ulkeler_comboBox.addItem(ulke)
           
        self.ulkeler_comboBox.currentIndexChanged.connect(self.sehirKontrolu)

    def ayarlar(self):
        try:
            self.gorunum = self.settings.value("Ayarlar/gorunum")
           
            if self.gorunum != None:
                if len(self.gorunum) > 0:
                    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(self.gorunum))
                else:
                    self.cleanlooksGorunumu()
            else:
                self.cleanlooksGorunumu()
   
            self.ulkeler_comboBox.setCurrentIndex(int(self.settings.value("Ayarlar/ulke")))
            self.sehirler_comboBox.setCurrentIndex(int(self.settings.value("Ayarlar/sehir")))
            self.ilceler_comboBox.setCurrentIndex(int(self.settings.value("Ayarlar/ilce")))
   
            otomatikCalistir = int(self.settings.value("Ayarlar/otomatik_calistir"))
            if otomatikCalistir == 0:
                self.otomatik_calistir_checkBox.setChecked(False)
            if otomatikCalistir == 2:
                self.otomatik_calistir_checkBox.setChecked(True)
               
            self.otomatikCalistir()
           
            ikonGoster = int(self.settings.value("Ayarlar/ikon_goster"))
            if ikonGoster == 0:
                self.ikon_goster_checkBox.setChecked(False)
                self.sistem_tepsisinde_baslat_checkBox.setEnabled(False)
                self.sistem_tepsisinde_baslat_checkBox.setChecked(False)
                self.trayIcon.hide()
            if ikonGoster == 2:
                self.ikon_goster_checkBox.setChecked(True)
                self.sistem_tepsisinde_baslat_checkBox.setEnabled(True)
                self.trayIcon.show()
   
            self.sistemTepsisindeBaslat = int(self.settings.value("Ayarlar/sistem_tepsisinde_baslat"))
            if self.sistemTepsisindeBaslat == 0:
                self.sistem_tepsisinde_baslat_checkBox.setChecked(False)
   
            if self.sistemTepsisindeBaslat == 2:
                self.sistem_tepsisinde_baslat_checkBox.setChecked(True)
   
            otomatikGuncelle = int(self.settings.value("Ayarlar/otomatik_guncelle"))
            if otomatikGuncelle == 0:
                self.otomatik_guncellestir_checkBox.setChecked(False)
            if otomatikGuncelle == 2:
                self.otomatik_guncellestir_checkBox.setChecked(True)
   
            herZamanUstte = int(self.settings.value("Ayarlar/her_zaman_ustte"))
            if herZamanUstte == 0:
                self.her_zaman_ustte_checkBox.setChecked(False)
            if herZamanUstte == 2:
                self.her_zaman_ustte_checkBox.setChecked(True)
   
            self.besmeleIleBasla = int(self.settings.value("Ayarlar/besmele_ile_basla"))
            if self.besmeleIleBasla == 0:
                self.besmele_ile_basla_checkBox.setChecked(False)
            if self.besmeleIleBasla == 2:
                self.besmele_ile_basla_checkBox.setChecked(True)
               
            winampDuraklat = int(self.settings.value("Ayarlar/winamp_duraklat"))
            if winampDuraklat == 0:
                self.winamp_duraklat_checkBox.setChecked(False)
            if winampDuraklat == 2:
                self.winamp_duraklat_checkBox.setChecked(True)
   
            sabahEzaniOku = int(self.settings.value("Ayarlar/sabah_ezani_oku"))
            if sabahEzaniOku == 0:
                self.sabah_ezani_oku_checkBox.setChecked(False)
            if sabahEzaniOku == 2:
                self.sabah_ezani_oku_checkBox.setChecked(True)
               
            ogleEzaniOku = int(self.settings.value("Ayarlar/ogle_ezani_oku"))
            if ogleEzaniOku == 0:
                self.ogle_ezani_oku_checkBox.setChecked(False)
            if ogleEzaniOku == 2:
                self.ogle_ezani_oku_checkBox.setChecked(True)
               
            ikindiEzaniOku = int(self.settings.value("Ayarlar/ikindi_ezani_oku"))
            if ikindiEzaniOku == 0:
                self.ikindi_ezani_oku_checkBox.setChecked(False)
            if ikindiEzaniOku == 2:
                self.ikindi_ezani_oku_checkBox.setChecked(True)
               
            aksamEzaniOku = int(self.settings.value("Ayarlar/aksam_ezani_oku"))
            if aksamEzaniOku == 0:
                self.aksam_ezani_oku_checkBox.setChecked(False)
            if aksamEzaniOku == 2:
                self.aksam_ezani_oku_checkBox.setChecked(True)
               
            yatsiEzaniOku = int(self.settings.value("Ayarlar/yatsi_ezani_oku"))
            if yatsiEzaniOku == 0:
                self.yatsi_ezani_oku_checkBox.setChecked(False)
            if yatsiEzaniOku == 2:
                self.yatsi_ezani_oku_checkBox.setChecked(True)
               
            selaOku = int(self.settings.value("Ayarlar/sela_oku"))
            if selaOku == 0:
                self.sela_oku_checkBox.setChecked(False)
            if selaOku == 2:
                self.sela_oku_checkBox.setChecked(True)
   
            duaOku = int(self.settings.value("Ayarlar/dua_oku"))
            if duaOku == 0:
                self.dua_oku_checkBox.setChecked(False)
            if duaOku == 2:
                self.dua_oku_checkBox.setChecked(True)
   
            erkenUyari = int(self.settings.value("Ayarlar/erken_uyari"))
            if erkenUyari == 0:
                self.erken_uyari_checkBox.setChecked(False)
            if erkenUyari == 2:
                self.erken_uyari_checkBox.setChecked(True)
   
            erkenUyariSuresi = self.settings.value("Ayarlar/erken_uyari_suresi")
            self.erken_uyari_spinBox.setValue(int(erkenUyariSuresi))
           
            erkenUyariSela = int(self.settings.value("Ayarlar/erken_uyari_sela"))
            if erkenUyariSela == 0:
                self.erken_uyari_sela_checkBox.setChecked(False)
            if erkenUyariSela == 2:
                self.erken_uyari_sela_checkBox.setChecked(True)
           
            erkenUyariSuresiSela = self.settings.value("Ayarlar/erken_uyari_suresi_sela")
            self.erken_uyari_sela_spinBox.setValue(int(erkenUyariSuresiSela))
           
            uyariSesiCal = int(self.settings.value("Ayarlar/uyari_sesi_cal"))
            if uyariSesiCal == 0:
                self.uyari_sesi_checkBox.setChecked(False)
            if (erkenUyari == 2) and (uyariSesiCal == 2):
                self.uyari_sesi_checkBox.setChecked(True)
           
            hicriGunIlave = int(self.settings.value("Ayarlar/hicri_gun_ilave"))
           
            if hicriGunIlave == 0:
                self.hicri_gun_ekle_checkBox.setChecked(False)
            if hicriGunIlave == 2:
                self.hicri_gun_ekle_checkBox.setChecked(True)
               
            ilaveGunSayisi = self.settings.value("Ayarlar/ilave_gun_sayisi")
            self.hicri_tarih_gun_ekle_spinBox.setValue(int(ilaveGunSayisi))
   
            sesAyari = float(self.settings.value("Ses_Ayarlari/ses_ayari"))
            self.audioOutput.setVolume(sesAyari)
            self.volume = self.audioOutput.volume()
   
            sesDosyasiSabah = self.settings.value("Ses_Ayarlari/sabah")
            self.sesDosyasiKontrol(self.sabah_lineEdit, sesDosyasiSabah)
   
            sesDosyasiOgle = self.settings.value("Ses_Ayarlari/ogle")
            self.sesDosyasiKontrol(self.ogle_lineEdit, sesDosyasiOgle)
   
            sesDosyasiIkindi = self.settings.value("Ses_Ayarlari/ikindi")
            self.sesDosyasiKontrol(self.ikindi_lineEdit, sesDosyasiIkindi)
   
            sesDosyasiAksam = self.settings.value("Ses_Ayarlari/aksam")
            self.sesDosyasiKontrol(self.aksam_lineEdit, sesDosyasiAksam)
   
            sesDosyasiYatsi = self.settings.value("Ses_Ayarlari/yatsi")
            self.sesDosyasiKontrol(self.yatsi_lineEdit, sesDosyasiYatsi)
   
            sesDosyasiDua = self.settings.value("Ses_Ayarlari/dua")
            self.sesDosyasiKontrol(self.dua_lineEdit, sesDosyasiDua)
   
            sesDosyasiUyari = self.settings.value("Ses_Ayarlari/uyari")
            self.sesDosyasiKontrol(self.uyari_lineEdit, sesDosyasiUyari)
   
            sesDosyasiSela = self.settings.value("Ses_Ayarlari/sela")
            self.sesDosyasiKontrol(self.sela_lineEdit, sesDosyasiSela)
       
        except TypeError:
            if QtCore.QFile.exists(self.ayarDosyasi):
                QtGui.QMessageBox.information(self, "Bilgilendirme", "Ayar dosyasında bozukluk tespit edildiğinden silindi. \nAyarlarınızı yaptıktan sonra kaydetmelisiniz.", "Tamam")
               
                QtCore.QFile(self.ayarDosyasi).remove()
                self.varsayilanAyarlar()

    def sesDosyasiKontrol(self, lineEdit, sesDosyasi):
        try:
            if len(sesDosyasi) > 0:
                lineEdit.setText(sesDosyasi)
        except TypeError:
            pass

    def varsayilanAyarlar(self):
        self.labelTemizlik()
        self.statusbar.clearMessage()
       
        self.varsayilanAyarlariKopyala()

        self.settings = QtCore.QSettings(self.ontanimliAyarDosyasi, QtCore.QSettings.IniFormat)
       
        self.settings.setValue("Ayarlar/winamp_konum", None)
       
        if QtCore.QFile.exists(QtCore.QFile(self.ontanimliAyarDosyasi)):
            if QtCore.QFile.exists(QtCore.QFile(self.ayarDosyasi)):
                QtCore.QFile(self.ayarDosyasi).remove()
               
            if QtCore.QFile.exists(QtCore.QFile(PyVakitci.veritabaniDosyasi)):
                QtCore.QFile(PyVakitci.veritabaniDosyasi).remove()

            self.ayarlar()

    def sesVarsayilanAyarlar(self):
        self.sabah_lineEdit.setText(self.sesDosyalariKonum + "sabah_saba.mp3")
        self.ogle_lineEdit.setText(self.sesDosyalariKonum + "ogle_rast.mp3")
        self.ikindi_lineEdit.setText(self.sesDosyalariKonum + "ikindi_hicaz.mp3")
        self.aksam_lineEdit.setText(self.sesDosyalariKonum + "aksam_segah.mp3")
        self.yatsi_lineEdit.setText(self.sesDosyalariKonum + "yatsi_ussak.mp3")
        self.dua_lineEdit.setText(self.sesDosyalariKonum + "ezan_duasi.mp3")
        self.uyari_lineEdit.setText(self.sesDosyalariKonum + "uyari.mp3")
        self.sela_lineEdit.setText(self.sesDosyalariKonum + "sela.mp3")

    def ayarlariUygula(self):
        if QtCore.QFile.exists(QtCore.QFile(self.ayarDosyasi)):
            self.settings = QtCore.QSettings(self.ayarDosyasi, QtCore.QSettings.IniFormat)
           
            self.ayarlar()
            self.vakitleriAl()
        else:
            self.settings = QtCore.QSettings(self.ontanimliAyarDosyasi, QtCore.QSettings.IniFormat)
            self.sesVarsayilanAyarlar()
            self.varsayilanAyarlar()

    def ayarlariKaydet(self):
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)

        self.calismaDizininiHazirla()
       
        self.settings = QtCore.QSettings(self.ayarDosyasi, QtCore.QSettings.IniFormat)

        self.settings.setValue("Ayarlar/gorunum", self.gorunum)
        self.settings.setValue("Ayarlar/ulke", self.ulkeler_comboBox.currentIndex())
        self.settings.setValue("Ayarlar/sehir", self.sehirler_comboBox.currentIndex())
        self.settings.setValue("Ayarlar/ilce", self.ilceler_comboBox.currentIndex())
        self.settings.setValue("Ayarlar/otomatik_calistir", self.otomatik_calistir_checkBox.checkState())
        self.otomatikCalistir()
        self.settings.setValue("Ayarlar/ikon_goster", self.ikon_goster_checkBox.checkState())
        self.settings.setValue("Ayarlar/sistem_tepsisinde_baslat", self.sistem_tepsisinde_baslat_checkBox.checkState())
        self.settings.setValue("Ayarlar/otomatik_guncelle", self.otomatik_guncellestir_checkBox.checkState())
        self.otomatikGuncellestir()
        self.settings.setValue("Ayarlar/her_zaman_ustte", self.her_zaman_ustte_checkBox.checkState())
        self.settings.setValue("Ayarlar/besmele_ile_basla", self.besmele_ile_basla_checkBox.checkState())
        self.settings.setValue("Ayarlar/winamp_duraklat", self.winamp_duraklat_checkBox.checkState())
        self.settings.setValue("Ayarlar/sabah_ezani_oku", self.sabah_ezani_oku_checkBox.checkState())
        self.settings.setValue("Ayarlar/ogle_ezani_oku", self.ogle_ezani_oku_checkBox.checkState())
        self.settings.setValue("Ayarlar/ikindi_ezani_oku", self.ikindi_ezani_oku_checkBox.checkState())
        self.settings.setValue("Ayarlar/aksam_ezani_oku", self.aksam_ezani_oku_checkBox.checkState())
        self.settings.setValue("Ayarlar/yatsi_ezani_oku", self.yatsi_ezani_oku_checkBox.checkState())
        self.settings.setValue("Ayarlar/dua_oku", self.dua_oku_checkBox.checkState())
        self.settings.setValue("Ayarlar/sela_oku", self.sela_oku_checkBox.checkState())      
        self.settings.setValue("Ayarlar/uyari_sesi_cal", self.uyari_sesi_checkBox.checkState())
        self.settings.setValue("Ayarlar/erken_uyari", self.erken_uyari_checkBox.checkState())
        self.settings.setValue("Ayarlar/erken_uyari_suresi", self.erken_uyari_spinBox.text())
        self.settings.setValue("Ayarlar/erken_uyari_sela", self.erken_uyari_sela_checkBox.checkState())
        self.settings.setValue("Ayarlar/erken_uyari_suresi_sela", self.erken_uyari_sela_spinBox.text())
        self.settings.setValue("Ayarlar/hicri_gun_ilave", self.hicri_gun_ekle_checkBox.checkState())
        self.settings.setValue("Ayarlar/ilave_gun_sayisi", self.hicri_tarih_gun_ekle_spinBox.text())
        self.settings.setValue("Ayarlar/uyari_sesi_cal", self.uyari_sesi_checkBox.checkState())
        self.settings.setValue("Ses_Ayarlari/sabah", self.sabah_lineEdit.text())
        self.settings.setValue("Ses_Ayarlari/ogle", self.ogle_lineEdit.text())
        self.settings.setValue("Ses_Ayarlari/ikindi", self.ikindi_lineEdit.text())
        self.settings.setValue("Ses_Ayarlari/aksam", self.aksam_lineEdit.text())
        self.settings.setValue("Ses_Ayarlari/yatsi", self.yatsi_lineEdit.text())
        self.settings.setValue("Ses_Ayarlari/dua", self.dua_lineEdit.text())
        self.settings.setValue("Ses_Ayarlari/uyari", self.uyari_lineEdit.text())
        self.settings.setValue("Ses_Ayarlari/sela", self.sela_lineEdit.text())
        self.settings.setValue("Ses_Ayarlari/ses_ayari", self.audioOutput.volume())
        self.volume = self.audioOutput.volume()
       
        self.hicriTarihiGuncelle()
       
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)

        self.vakitleriAl()
   
    def veritabaniniGuncelle(self):
        try:
            if self.timerLabel.isActive():
                self.timerLabel.stop()
        except AttributeError:
            pass
       
        self.diyanetAylikVakitleriKaydet()
       
    def yerKontrol(self, veri):
        if len(veri) > 0:
            return veri
        else:
            return None
       
    def ulkeSehirBilgisiniAl(self):
        self.ulke = self.ulkeler_comboBox.currentText()
        self.sehir = self.sehirler_comboBox.currentText()
        self.ilce = self.ilceler_comboBox.currentText()
       
        self.ulke_label.setText(self.ulke)
        self.sehir_label.setText(self.sehir)
       
        Vakitler.ulke = self.diyanetUlkeler.ulkeler.get(self.ulke)
        if self.yerKontrol(self.sehir) != None:
            Vakitler.sehir = self.sehirler.get(self.sehir)
        else:
            Vakitler.sehir = None
       
        if self.yerKontrol(self.ilce) != None:
            Vakitler.ilce = self.ilceler.get(self.ilce)
            Vakitler.link = self.linkler.get(self.ilce)
        else:
            Vakitler.ilce = None
           
        Vakitler.seciliSehir = self.sehir
       
    def vakitleriAl(self):
        self.labelTemizlik()
        self.statusbar.clearMessage()
       
        self.ulkeSehirBilgisiniAl()
       
        if len(self.ulke) > 0 and len(self.sehir) > 0:

            if QtCore.QFile.exists(self.veritabaniDosyasi) == False:
                self.diyanetAylikVakitleriKaydet()
            else:
                if QtCore.QFile(self.veritabaniDosyasi).size() == 2048:
                    if QtCore.QFile.exists(self.veritabaniDosyasi):
                        QtCore.QFile(self.veritabaniDosyasi).remove()
                       
                    self.diyanetAylikVakitleriKaydet()
           
            if self.ulkeler_comboBox.currentIndex() >= 0:
                if self.sehirler_comboBox.currentIndex() >= 0:
                    if self.rlock._is_owned() == False:
                        vakitler = Vakitler(self, self.sehir)
                        vakitler.start()
           
            self.timerLabel = QtCore.QTimer()
            self.timerLabel.timeout.connect(self.labelGuncelle)
            self.timerLabel.start(500)
       
    def gunlukVakitleriKaydet(self):
        if len(Vakitler.saatler) != 0:
            self.settings.setValue("Vakitler/imsak", Vakitler.imsak)
            self.settings.setValue("Vakitler/gunes", Vakitler.gunes)
            self.settings.setValue("Vakitler/ogle", Vakitler.ogle)
            self.settings.setValue("Vakitler/ikindi", Vakitler.ikindi)
            self.settings.setValue("Vakitler/aksam", Vakitler.aksam)
            self.settings.setValue("Vakitler/yatsi", Vakitler.yatsi)
            self.settings.setValue("Vakitler/sela", self.erken_uyari_sela_spinBox.text())

    def labelGuncelle(self):
        self.saat = QtCore.QTime().currentTime().toString("hh:mm")
       
        if len(Vakitler.saatler) != 0:
            self.statusbar.showMessage("Kaynak: diyanet.gov.tr")
           
            self.gunlukVakitleriKaydet()
           
            try:
                if "00:00" <= self.saat < Vakitler.imsak:
                    self.labelVeriler(Vakitler.imsak, Vakitler.gunes, Vakitler.ogle, Vakitler.ikindi,
                                      Vakitler.aksam, "<font color='#FF0000'>" + Vakitler.yatsi + "</font>",
                                      "Şimdi Yatsı Vakti", "İmsak'a Kalan Süre :", "yatsı")

                if Vakitler.imsak <= self.saat < Vakitler.gunes:
                    self.labelVeriler("<font color='#FF0000'>" + Vakitler.imsak + "</font>", Vakitler.gunes,
                                      Vakitler.ogle, Vakitler.ikindi, Vakitler.aksam, Vakitler.yatsi,
                                      "Şimdi İmsak Vakti", "Güneş'e Kalan Süre :", "sabah")

                    self.diniGunleriHatirlat()

                    self.vakitKontrol("Namaz Vakti", self.sabah_lineEdit.text(), self.imsak_saat_label.text(), "sabah")

                if Vakitler.gunes <= self.saat < Vakitler.ogle:
                    self.labelVeriler(Vakitler.imsak, "<font color='#FF0000'>" + Vakitler.gunes + "</font>",
                                      Vakitler.ogle, Vakitler.ikindi, Vakitler.aksam, Vakitler.yatsi,
                                      "Şimdi Güneş Vakti", "Öğle'ye Kalan Süre :", "güneş")

                if Vakitler.ogle <= self.saat < Vakitler.ikindi:
                    self.labelVeriler(Vakitler.imsak, Vakitler.gunes, "<font color='#FF0000'>" + Vakitler.ogle + "</font>",
                                      Vakitler.ikindi, Vakitler.aksam, Vakitler.yatsi, "Şimdi Öğle Vakti",
                                      "İkindi'ye Kalan Süre :", "öğle")

                    self.diniGunleriHatirlat()

                    self.vakitKontrol("Namaz Vakti", self.ogle_lineEdit.text(), self.ogle_saat_label.text(), "öğle")

                if Vakitler.ikindi <= self.saat < Vakitler.aksam:
                    self.labelVeriler(Vakitler.imsak, Vakitler.gunes, Vakitler.ogle,
                                      "<font color='#FF0000'>" + Vakitler.ikindi + "</font>", Vakitler.aksam,
                                      Vakitler.yatsi, "Şimdi İkindi Vakti", "Akşam'a Kalan Süre :", "ikindi")

                    self.diniGunleriHatirlat()

                    self.vakitKontrol("Namaz Vakti", self.ikindi_lineEdit.text(), self.ikindi_saat_label.text(), "ikindi")

                if Vakitler.aksam <= self.saat < Vakitler.yatsi:
                    self.labelVeriler(Vakitler.imsak, Vakitler.gunes, Vakitler.ogle, Vakitler.ikindi,
                                      "<font color='#FF0000'>" + Vakitler.aksam + "</font>", Vakitler.yatsi,
                                      "Şimdi Akşam Vakti", "Yatsı'ya Kalan Süre :", "akşam")

                    self.diniGunleriHatirlat()

                    self.vakitKontrol("Namaz Vakti", self.aksam_lineEdit.text(), self.aksam_saat_label.text(), "akşam")

                if Vakitler.yatsi <= self.saat <= "23:59":
                    self.labelVeriler(Vakitler.imsak, Vakitler.gunes, Vakitler.ogle, Vakitler.ikindi,
                                      Vakitler.aksam, "<font color='#FF0000'>" + Vakitler.yatsi + "</font>",
                                      "Şimdi Yatsı Vakti", "İmsak'a Kalan Süre :", "yatsı")

                    self.diniGunleriHatirlat()

                    self.vakitKontrol("Namaz Vakti", self.yatsi_lineEdit.text(), self.yatsi_saat_label.text(), "yatsı")
            except ValueError:
                pass

        else:
            if Vakitler.tarihHatasi:
                self.timerLabel.stop()
                self.statusbar.clearMessage()
                QtGui.QMessageBox.warning(self, "Tarih Hatası",
                                                "Sisteminizin tarihi yanlış. Tarihi düzelttikten sonra veya \"Vakitleri aylık olarak al.\" " +
                                                "seçeneğinin işaretini kaldırdıktan sonra Ayarlar sekmesindeki Kaydet butonuna tıklayın.",
                                                "Tamam")
            else:
                Vakitler.tarihHatasi = False
               
        if Vakitler.veritabanindakiYerBilgisi == False:
            self.veritabaniniGuncelle()

    def labelVeriler(self, imsak, gunes, ogle, ikindi, aksam, yatsi, namazvakti, sonrakivakit, simdikivakit):
        self.imsak_saat_label.setText(imsak)
        self.gunes_saat_label.setText(gunes)
        self.ogle_saat_label.setText(ogle)
        self.ikindi_saat_label.setText(ikindi)
        self.aksam_saat_label.setText(aksam)
        self.yatsi_saat_label.setText(yatsi)
        self.namaz_vakti_label.setText(namazvakti)
        self.namazvakti = namazvakti
        self.sonraki_vakit_label.setText(sonrakivakit)

        self.kalanSureKontrol(simdikivakit)

    def kalanSureKontrol(self, vakit):
        self.simdikiZaman = QtCore.QTime().currentTime()
        self.simdikiSaat = int(self.simdikiZaman.toString("hh"))
        self.simdikiDakika = int(self.simdikiZaman.toString("mm"))
        self.simdikiSaniye = int(self.simdikiZaman.toString("ss"))

        if vakit == "sabah":
            gunes = str(self.gunes_saat_label.text())
            saat = int(gunes[:gunes.find(":")].replace("<font color='#FF0000'>", ""))
            dakika = int(gunes[gunes.find(":") + 1:].replace("</font>", ""))

            self.toplamDakika = (saat * 60 + dakika) - (self.simdikiSaat * 60 + self.simdikiDakika)
            self.erkenUyariKontrol(self.toplamDakika)

        if vakit == "güneş":
            ogle = str(self.ogle_saat_label.text())
            saat = int(ogle[:ogle.find(":")].replace("<font color='#FF0000'>", ""))
            dakika = int(ogle[ogle.find(":") + 1:].replace("</font>", ""))

            self.toplamDakika = (saat * 60 + dakika) - (self.simdikiSaat * 60 + self.simdikiDakika)
            self.erkenUyariKontrol(self.toplamDakika)

        if vakit == "öğle":
            ikindi = str(self.ikindi_saat_label.text())
            saat = int(ikindi[:ikindi.find(":")].replace("<font color='#FF0000'>", ""))
            dakika = int(ikindi[ikindi.find(":") + 1:].replace("</font>", ""))

            self.toplamDakika = (saat * 60 + dakika) - (self.simdikiSaat * 60 + self.simdikiDakika)
            self.erkenUyariKontrol(self.toplamDakika)

        if vakit == "ikindi":
            aksam = str(self.aksam_saat_label.text())
            saat = int(aksam[:aksam.find(":")].replace("<font color='#FF0000'>", ""))
            dakika = int(aksam[aksam.find(":") + 1:].replace("</font>", ""))

            self.toplamDakika = (saat * 60 + dakika) - (self.simdikiSaat * 60 + self.simdikiDakika)
            self.erkenUyariKontrol(self.toplamDakika)

        if vakit == "akşam":
            yatsi = str(self.yatsi_saat_label.text())
            saat = int(yatsi[:yatsi.find(":")].replace("<font color='#FF0000'>", ""))
            dakika = int(yatsi[yatsi.find(":") + 1:].replace("</font>", ""))

            self.toplamDakika = (saat * 60 + dakika) - (self.simdikiSaat * 60 + self.simdikiDakika)
            self.erkenUyariKontrol(self.toplamDakika)

        if vakit == "yatsı":
            imsak = str(self.imsak_saat_label.text())
            saat = int(imsak[:imsak.find(":")].replace("<font color='#FF0000'>", ""))
            dakika = int(imsak[imsak.find(":") + 1:].replace("</font>", ""))

            if saat >= self.simdikiSaat >= 0:
                self.toplamDakika = (saat * 60 + dakika) - (self.simdikiSaat * 60 + self.simdikiDakika)
                self.erkenUyariKontrol(self.toplamDakika)
            else:
                self.toplamDakika = (24 * 60) - (self.simdikiSaat * 60 + self.simdikiDakika) + (saat * 60 + dakika)
                self.erkenUyariKontrol(self.toplamDakika)

        self.kalanSureyiHesapla(saat, dakika)

    def kalanSureyiHesapla(self, saat, dakika):
        belirlenenSaat = int(saat)
        belirlenenDakika = int(dakika)

        belirlenenZaman = datetime.timedelta(0, 0, 0, 0, belirlenenDakika, belirlenenSaat, 0)
        simdi = datetime.timedelta(0, self.simdikiSaniye, 0, 0, self.simdikiDakika, self.simdikiSaat, 0)

        kalanSure = str(belirlenenZaman - simdi)

        # "-1 gün..." tarzında bir çıktı alma ihtimaline karşı önlem.
        kalanSure = kalanSure[kalanSure.rfind(" ") + 1:]

        self.kalan_sure_label.setText(kalanSure)

        kalanSaat = kalanSure[:kalanSure.find(":")]
        kalanDakika = kalanSure[kalanSure.find(":") + 1 : kalanSure.rfind(":")]
        
        if kalanSaat == "0":
            if self.sela_oku_checkBox.isChecked():
                self.selaOkuKontrol(kalanDakika)


    def erkenUyariKontrol(self, toplamDakika):
        try:
            if toplamDakika == int(self.erken_uyari_spinBox.text()):
                if self.erken_uyari_checkBox.isChecked():
                    if self.mesajGosterildi == False:
                        self.trayIcon.showMessage("Erken Uyarı",
                                                  self.sonraki_vakit_label.text() + " " + str(toplamDakika) + " Dakika",
                                                  self.trayIcon.Information, 20000)
                        self.mesajGosterildi = True
                        
                        if self.uyari_sesi_checkBox.isChecked():
                            self.sesDosyasiniAc(self.uyari_lineEdit.text())
   
                        self.timerMesaj()
        except:
            pass

    def mesajGoster(self, baslik, mesaj):
        self.trayIcon.showMessage(baslik, mesaj, self.trayIcon.Information, 20000)

    def vakitleriGoster(self):
        self.mesajGoster("Namaz Vakitleri", self.vakitlerMesaj())

    def vakitlerMesaj(self):
        try:
            mesaj = self.ilceler_comboBox.currentText() + " için " + self.namazvakti.replace("Şimdi ", "") + \
                    "\nİmsak: " + Vakitler.imsak + "\tGüneş: " + Vakitler.gunes + \
                    "\nÖğle: " + Vakitler.ogle + "\tİkindi: " + Vakitler.ikindi + \
                    "\nAkşam: " + Vakitler.aksam + "\tYatsı: " + Vakitler.yatsi
        except AttributeError:
            mesaj = "Namaz vakitleri alınamadı."

        return mesaj

    def vakitKontrol(self, baslik, dosya, labelsaat, simdikivakit):
        try:
            ara = re.search(">(.*)<", labelsaat)
            saat = ara.group(1)

            if saat == self.saat:
                if self.mesajGosterildi == False:
                    mesaj = self.vakitlerMesaj()
                    self.mesajGoster(baslik, mesaj)
                    self.mesajGosterildi = True
                   
                    if self.sabah_ezani_oku_checkBox.isChecked() or +\
                        self.ogle_ezani_oku_checkBox.isChecked() or  +\
                        self.ikindi_ezani_oku_checkBox.isChecked() or +\
                        self.aksam_ezani_oku_checkBox.isChecked() or +\
                        self.yatsi_ezani_oku_checkBox.isChecked():
                       
                            self.ezanOku(dosya)

                    try:
                        self.timerMesaj()
                    except TypeError:
                        pass
        except:
            pass

    def timerMesaj(self):
        self.timerMesaj = QtCore.QTimer()
        self.timerMesaj.timeout.connect(self.mesajGosterimKontrol)
        self.timerMesaj.start(120000)

    def mesajGosterimKontrol(self):
        self.mesajGosterildi = False
        self.timerMesaj.stop()

    def sesDosyasiniAc(self, dosya):
        self.mediaNesnesi.setCurrentSource(Phonon.MediaSource(dosya))

        try:
            self.mediaNesnesi.stop()
        except:
            pass

        self.mediaNesnesi.play()

    def ezanOku(self, dosya):
        if self.winamp_duraklat_checkBox.isChecked():
            self.winampKontrol.duraklat()
       
        self.sesDosyasiniAc(dosya)
        self.mediaNesnesi.finished.connect(self.ezanDuasiniOku)

    def ezanDuasiniOku(self):
        if self.dua_oku_checkBox.isChecked():
            self.mediaNesnesi.setCurrentSource(Phonon.MediaSource(self.dua_lineEdit.text()))

            try:
                self.mediaNesnesi.stop()
            except:
                pass

            self.mediaNesnesi.play()
            self.mediaNesnesi.finished.connect(self.sesDosyasiOynatmaBitti)
        else:
            self.sesDosyasiOynatmaBitti()
   
    def sesDosyasiOynatmaBitti(self):
        self.mediaNesnesi.stop()
       
        if self.winamp_duraklat_checkBox.isChecked():
            self.winampKontrol.oynat()

    def selaOkuKontrol(self, dakika):
        gun = QtCore.QDate().currentDate().toString("dddd")
        
        try:
            if gun == "Cuma":
                if self.namaz_vakti_label.text() == "Şimdi Güneş Vakti":
                    if dakika == self.erken_uyari_sela_spinBox.text():
                        if self.mesajGosterildi == False:
                            self.mesajGoster("Hâyırlı Cumalar", "\nSela okunuyor.")
                            self.mesajGosterildi = True
    
                            self.selaOku()
                            self.timerMesaj()
        except:
            pass

    def selaOku(self):
        if self.winamp_duraklat_checkBox.isChecked():
            self.winampKontrol.duraklat()
           
        self.selaDosyasi = self.sela_lineEdit.text()
        self.sesDosyasiniAc(self.selaDosyasi)
        self.mediaNesnesi.finished.connect(self.sesDosyasiOynatmaBitti)

    def ulkeKontrolu(self):
        secilenUlke = self.ulkeler_comboBox.currentText()

        if (secilenUlke == "ABD") or (secilenUlke == "KANADA") or (secilenUlke == "TÜRKİYE"):
            return True

    def sehirKontrolu(self):
        self.sehirler_comboBox.clear()
        self.sehirleriAl()
   
    def sehirleriAl(self):
        self.sehirler = None
       
        if self.ulkeler_comboBox.currentIndex() > -1:
            if self.siteyeBaglantiVarMi(self.diyanetURL):
                sehirleriAl = SehirleriAl(self.ulkeler_comboBox.currentText())
                self.sehirler = sehirleriAl.basla()
            else:
                self.sehirler = self.settings.value("Diyanet/sehirler")
               
            if len(self.sehirler.keys()) > 0:
                self.sehirleriEkle()
       
    def sehirleriEkle(self):
        for sehir in sorted(self.sehirler):
            self.sehirler_comboBox.addItem(sehir)
       
        self.sehirler_comboBox.currentIndexChanged.connect(self.ilceKontrolu)
       
    def ilceKontrolu(self):
        self.ilceler_comboBox.clear()

        if self.ulkeKontrolu():
            self.ilceler_comboBox.setEnabled(True)
            self.ilceleriAl()
        else:
            self.ilceler_comboBox.setEnabled(False)
   
    def ilceleriAl(self):
        self.ilceler = None
       
        if self.sehirler_comboBox.currentIndex() > -1:
            if self.siteyeBaglantiVarMi(self.diyanetURL):
                ilceleriAl = IlceleriAl(self.sehirler, self.ulkeler_comboBox.currentText(), self.sehirler_comboBox.currentText())
                data = ilceleriAl.basla()
                
                self.ilceler = data[0]
                self.linkler = data[1]
            else:
                self.ilceler = self.settings.value("Diyanet/ilceler")
                self.linkler = self.settings.value("Diyanet/linkler")
               
            if len(self.ilceler.keys()) > 0:
                self.ilceleriEkle()
           
    def ilceleriEkle(self):
        for ilce in sorted(self.ilceler):
            self.ilceler_comboBox.addItem(ilce)

    def labelAdiniDegistir(self, secilenUlke):
        if self.ulkeKontrolu():
            if (secilenUlke == "ABD") or (secilenUlke == "KANADA"):
                self.bolgesel_ayarlar_sehir_label.setText("Eyalet:")
                self.bolgesel_ayarlar_ilce_label.setText("Şehir:")
            else:
                self.bolgesel_ayarlar_sehir_label.setText("Şehir:")
                self.bolgesel_ayarlar_ilce_label.setText("İlçe:")
        else:
            self.bolgesel_ayarlar_sehir_label.setText("Şehir:")
            self.bolgesel_ayarlar_ilce_label.setText("İlçe:")

    def vakitleriTopluGoster(self):
        if QtCore.QFile(self.veritabaniDosyasi).size() >= 4096:
            AylikVakitler(self.veritabaniDosyasi)

            if Vakitler.tarihHatasi == True:
                self.timerLabel.stop()
                self.statusbar.clearMessage()
                QtGui.QMessageBox.warning(self, "Tarih Hatası",
                                          'Sisteminizin tarihi yanlış. Tarihi düzelttikten sonra veya "Vakitleri aylık olarak al." ' +
                                           "seçeneğinin işaretini kaldırdıktan sonra Ayarlar sekmesindeki Kaydet butonuna tıklayın" +
                                           "veya programı tekrar çalıştırın.", "Tamam")

            if AylikVakitler.veritabaniVarmi == False:
                self.diyanetAylikVakitleriKaydet()
                AylikVakitler(self.veritabaniDosyasi)

        else:
            self.diyanetAylikVakitleriKaydet()
            AylikVakitler(self.veritabaniDosyasi)

    def siteyeBaglantiVarMi(self, url):
        siteyeBaglan = SiteyeBaglan(url)
        siteyeBaglan.start()
        siteyeBaglan.join(3)
       
        if siteyeBaglan.baglantiVarmi:
            return True
        else:
            return False

    def diyanetAylikVakitleriKaydet(self):
        if self.siteyeBaglantiVarMi(self.diyanetURL):
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.BusyCursor)

            self.statusbar.showMessage("Vakitler güncelleniyor...")
           
            vakitler = Vakitler(PyVakitci, self.sehir)

            ulke = self.ulkeler_comboBox.currentText()

            if self.ulkeKontrolu():
                if ulke == "TÜRKİYE":
                    vakitler.diyanetAylikVakitleriKaydet("İlçe")
                else:
                    vakitler.diyanetAylikVakitleriKaydet("Şehir")
            else:
                vakitler.diyanetAylikVakitleriKaydet("Şehir")

            self.statusbar.clearMessage()

            QtGui.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)

            self.vakitleriAl()

        else:
            self.statusbar.clearMessage()
            QtGui.QMessageBox.warning(self, "Bağlantı Hatası",
                                            "Diyanetin sitesine bağlantı kurulamadığından dolayı \n" +
                                            "namaz vakitleri veritabanı güncellenemedi.",
                                            "Tamam")
            
    def siteAc(self, url):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def lisans(self):
        dosyaIsmi = self.lisansDosyasi[self.lisansDosyasi.rfind("/") + 1:]
        dosyaKonumu = self.lisansDosyasi[:self.lisansDosyasi.rfind("/")]
        os.chdir(dosyaKonumu)
        self.siteAc(dosyaIsmi)

    def hakkindaDialog(self):
        from moduller.Hakkinda import Hakkinda
        dialog = Hakkinda()
        dialog.exec_()

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            event.ignore()
            self.setVisible(False)
        else:
            sys.exit(0)

    def programiKapat(self):
        self.trayIcon.hide()
        sys.exit(0)

if __name__ == "__main__":
    uygulama = QtGui.QApplication(sys.argv)
    uygulama.setApplicationName("PyVakitci")
