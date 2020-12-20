# -*- coding: utf-8 -*-

# Hazırlayan : Rahman Yazgan (rahmanyazgan@gmail.com)
# Lisans : GPL v.3

import json, requests
from PyQt4 import QtCore
from moduller.SiteyeBaglan import SiteyeBaglan
from moduller.DiyanetUlkeler import DiyanetUlkeler

class IlceleriAl:
    ayarDosyasi = None
    
    def __init__(self, sehirlerListesi, sehir):
        self.sehirler = sehirlerListesi
        self.sehir = sehir
        
    def siteyeBaglantiVarMi(self, url):
        siteyeBaglan = SiteyeBaglan(url)
        siteyeBaglan.start()
        siteyeBaglan.join(3)
        
        if siteyeBaglan.baglantiVarmi:
            return True
        else:
            return False

    def basla(self):
        url = DiyanetUlkeler.CITY_URL
        
        if self.siteyeBaglantiVarMi(url):
            url = url
        else:
            url = DiyanetUlkeler.CITY_URL_NEW
        
        try:
            response = requests.get(url=url, params={"itemId" : self.sehirler.get(self.sehir)})
            veriler = json.loads(response.text)
            
            ilceler = {}
            
            for i in range(0, len(veriler), 1):
                ilceler.__setitem__(veriler[i].get("Text"), veriler[i].get("Value"))
                
            self.settings = QtCore.QSettings(IlceleriAl.ayarDosyasi, QtCore.QSettings.IniFormat)
            self.settings.setValue("Diyanet/ilceler", ilceler)
        
        except:
            ilceler = None
        
        return ilceler