# -*- coding: utf-8 -*-

# Hazırlayan : Rahman Yazgan (rahmanyazgan@gmail.com)
# Lisans : GPL v.3

from PyQt4 import QtGui, QtCore
import re, sqlite3, threading, urllib.parse, urllib.request

from moduller.SiteyeBaglan import SiteyeBaglan
from moduller.DiyanetUlkeler import DiyanetUlkeler

class Vakitler(threading.Thread):
    baglantiSorunu = None
    simdikiTarih = None
    saatler = None
    imsak = None
    gunes = None
    ogle = None
    ikindi = None
    aksam = None
    yatsi = None
    ulke = None
    sehir = None
    seciliSehir = None
    ilce = None
    tarihHatasi = None
    veritabanindakiYerBilgisi = None
    veritabanindakiYer = None

    def __init__(self, sinif, sehir):
        threading.Thread.__init__(self)
        
        self.pyvakitci = sinif
        Vakitler.seciliSehir = sehir
        Vakitler.veritabaniSehir = sehir
        self.diyanetUlkeler = DiyanetUlkeler()
        
    def siteyeBaglantiVarMi(self, url):
        siteyeBaglan = SiteyeBaglan(url)
        siteyeBaglan.start()
        siteyeBaglan.join(3)
        
        if siteyeBaglan.baglantiVarmi:
            return True
        else:
            return False

    def run(self):
        self.pyvakitci.rlock.acquire()

        Vakitler.saatler = ""
        Vakitler.imsak = ""
        Vakitler.gunes = ""
        Vakitler.ogle = ""
        Vakitler.ikindi = ""
        Vakitler.aksam = ""
        Vakitler.yatsi = ""

        self.diyanetAylikVakitleriAl()

        self.pyvakitci.rlock.release()

    def diyanetAylikVakitleriAl(self):
        if QtCore.QFile.exists(self.pyvakitci.veritabaniDosyasi):
            if QtCore.QFile(self.pyvakitci.veritabaniDosyasi).size() >= 4096:
                
                connect = sqlite3.connect(self.pyvakitci.veritabaniDosyasi)
                cursor = connect.cursor()

                try:
                    cursor.execute("SELECT " + self.ilceSehirKontrolu() + " FROM namazvakitleri")
                    yerBilgisi = str(cursor.fetchone())
                    
                    yerBilgisi = yerBilgisi[2:yerBilgisi.rfind("'")]
                    
                    if yerBilgisi == Vakitler.seciliSehir:
                        try:
                            cursor.execute("SELECT Tarih FROM namazvakitleri")
                            veriler = cursor.fetchall()
                            
                            tarihler = []
                            vakitler = []

                            for tarih in veriler:
                                tarihler.append(str(tarih[0]))

                            if tarihler.count(self.simdikiTarih) == 1:
                                cursor.execute("SELECT İmsak, Güneş, Öğle, İkindi, Akşam, Yatsı, Kıble FROM namazvakitleri WHERE tarih = '" + str(self.simdikiTarih) + "'")
                                veriler = cursor.fetchone()
                                
                                for vakit in veriler:
                                    vakitler.append(str(vakit))

                                Vakitler.saatler = vakitler
                                Vakitler.imsak = vakitler[0]
                                Vakitler.gunes = vakitler[1]
                                Vakitler.ogle = vakitler[2]
                                Vakitler.ikindi = vakitler[3]
                                Vakitler.aksam = vakitler[4]
                                Vakitler.yatsi = vakitler[5]
                                
                                Vakitler.tarihDogrumu = True
                            else:
                                Vakitler.tarihDogrumu = False

                                self.diyanetAylikVakitleriKaydet(self.ilceSehirKontrolu())
                                self.run()

                            Vakitler.veritabanindakiYerBilgisi = True
                            Vakitler.veritabanindakiYer = yerBilgisi

                        except sqlite3.OperationalError:
                            self.diyanetAylikVakitleriKaydet(self.ilceSehirKontrolu())
                            self.run()

                        Vakitler.veritabanindakiYerBilgisi = True
                        Vakitler.veritabanindakiYer = yerBilgisi
                    else:
                        Vakitler.veritabanindakiYerBilgisi = False
                        Vakitler.veritabanindakiYer = yerBilgisi
                except sqlite3.OperationalError:
                    self.diyanetAylikVakitleriKaydet(self.ilceSehirKontrolu())
                    self.run()

    def ilceSehirKontrolu(self):
        if Vakitler.ulke == "TÜRKİYE":
            return "İlçe"
        else:
            return "Şehir"

    def diyanetAylikVakitleriKaydet(self, ilceSehir):
        url = "http://www.diyanet.gov.tr"
        
        try:
            if (Vakitler.ulke != None) or (Vakitler.sehir != None):
                if self.siteyeBaglantiVarMi(url):
                    if QtCore.QFile.exists(self.pyvakitci.veritabaniDosyasi):
                        QtCore.QFile(self.pyvakitci.veritabaniDosyasi).remove()
            
                    connect = sqlite3.connect(self.pyvakitci.veritabaniDosyasi)
                    cursor = connect.cursor()
            
                    sqlString = "DROP TABLE namazvakitleri"
            
                    try:
                        try:
                            cursor.execute(sqlString)
                        except sqlite3.OperationalError:
                            pass
                            #print("namazvakitleri tablosu yok.")
            
                        sqlString = "CREATE TABLE namazvakitleri (" + str(ilceSehir) + ", Tarih, İmsak, Güneş, Öğle, İkindi, Akşam, Yatsı, Kıble)"
                        cursor.execute(sqlString)
            
                    except sqlite3.OperationalError:
                        pass
                        #print("namazvakitleri tablosu zaten var.")
                    
                    url = self.diyanetUlkeler.PRAYER_POST_URL
                    
                    if self.siteyeBaglantiVarMi("http://www.diyanet.gov.tr/tr/PrayerTime"):
                        url = url
                    else:
                        url = self.diyanetUlkeler.PRAYER_POST_URL_NEW
                    
                    country = Vakitler.ulke
                    state = Vakitler.sehir
                    city = Vakitler.ilce
                    
                    if Vakitler.ilce != None:
                        values = {'country': country, 'state': state, 'city': city, 'period': "Aylik"}
                    else:
                        values = {'country': country, 'state': state, 'period': "Aylik"}
                    
                    try:
                        data = urllib.parse.urlencode(values)
                        binary_data = data.encode('UTF-8')
                        request = urllib.request.Request(url, binary_data)
                        response = urllib.request.urlopen(request)
                        
                        html = response.read()
                        
                        derle = re.compile("[0-3]+[0-9][.][0-2][0-9][.][0-2]+[0-9]")
                        tarihler = derle.findall(str(html))
                        
                        
                        if tarihler.count(Vakitler.simdikiTarih) == 0:
                            Vakitler.tarihHatasi = True
                            QtCore.QFile(self.pyvakitci.veritabaniDosyasi).remove()
                        else:
                            derle = re.compile('<td class="tCenter">(.*?)</td>')
                            saatler = derle.findall(str(html))
            
                            i = 0
                            j = 0
                            while i < 240:
                                imsak = saatler[i+1]
                                gunes = saatler[i+2]
                                ogle = saatler[i+3]
                                ikindi = saatler[i+4]
                                aksam = saatler[i+5]
                                yatsi = saatler[i+6]
                                kıbleSaati = saatler[i+7]
        
                                sqlString = "INSERT INTO namazvakitleri VALUES ('" + \
                                                str(self.veritabaniSehir) + "', '" + tarihler[j] + "', '" + \
                                                imsak + "', '" + gunes + "', '" + ogle + "', '" + \
                                                ikindi + "', '" + aksam + "', '" + yatsi + "', '" + \
                                                kıbleSaati + "')"
            
                                cursor.execute(sqlString)
            
                                i = i + 8
                                j = j + 1
                                
                        connect.commit()
                        Vakitler.tarihHatasi = False
                    except:
                        pass
                else:
                    QtGui.QMessageBox.information(self, "Bilgilendirme", "Diyanetin sitesine bağlanılamadığından vakitler alınamadı/güncellenemedi.","Tamam")
        except:
            pass
