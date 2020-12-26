# -*- coding: utf-8 -*-

# Hazırlayan : Rahman Yazgan (rahmanyazgan@gmail.com)
# Lisans : GPL v.3

import datetime, re, requests, sqlite3, threading
from PyQt4 import QtGui, QtCore
from bs4 import BeautifulSoup

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
                                cursor.execute("SELECT İmsak, Güneş, Öğle, İkindi, Akşam, Yatsı FROM namazvakitleri WHERE tarih = '" + str(self.simdikiTarih) + "'")
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
        url = DiyanetUlkeler.BASE_URL
        
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
            
                        sqlString = "CREATE TABLE namazvakitleri (" + str(ilceSehir) + ", Tarih, İmsak, Güneş, Öğle, İkindi, Akşam, Yatsı)"
                        cursor.execute(sqlString)
            
                    except sqlite3.OperationalError:
                        pass
                        #print("namazvakitleri tablosu zaten var.")
                    
                    #try:
                    url = url + Vakitler.link
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, "html.parser")
                    table = soup.find_all("table", class_="vakit-table")
                    aylik_vakitler = table[1].find_all("tr")
                    
                    if len(aylik_vakitler) > 0:
                        aylik_vakitler.remove(aylik_vakitler[0])
                        
                        temp_date = datetime.datetime.now()
                        
                        for item in aylik_vakitler:
                            data = re.match("\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n(.*?)\n", item.getText()).groups()
                            
                            if len(data) > 0:
                                tarih = temp_date.date().strftime('%d.%m.%Y') 
                                imsak = data[1]
                                gunes = data[2]
                                ogle = data[3]
                                ikindi = data[4]
                                aksam = data[5]
                                yatsi = data[6]
                                
                                sqlString = "INSERT INTO namazvakitleri VALUES ('" + \
                                    str(self.veritabaniSehir) + "', '" + tarih + "', '" + \
                                    imsak + "', '" + gunes + "', '" + ogle + "', '" + \
                                    ikindi + "', '" + aksam + "', '" + yatsi + "')"
                                    
                                cursor.execute(sqlString)
                                
                                temp_date = temp_date + datetime.timedelta(days=1)
                        
                        connect.commit()
                        
                        Vakitler.tarihHatasi = False
                    #except:
                    #    pass
                else:
                    QtGui.QMessageBox.information(self, "Bilgilendirme", "Diyanetin sitesine bağlanılamadığından vakitler alınamadı/güncellenemedi.","Tamam")
        except:
            pass