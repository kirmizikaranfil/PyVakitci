# -*- coding: utf-8 -*-

# Hazırlayan : Rahman Yazgan (rahmanyazgan@gmail.com)
# Lisans : GPL v.3

import json, requests
from moduller.SiteyeBaglan import SiteyeBaglan
from moduller.DiyanetUlkeler import DiyanetUlkeler

from PyQt4 import QtCore

class SehirleriAl:
    ulke = None
    ayarDosyasi = None
    
    def __init__(self, ulke):
        self.ulke = ulke
        
    def siteyeBaglantiVarMi(self, url):
        siteyeBaglan = SiteyeBaglan(url)
        siteyeBaglan.start()
        siteyeBaglan.join(3)
        
        if siteyeBaglan.baglantiVarmi:
            return True
        else:
            return False

    def basla(self):
        url = DiyanetUlkeler.COUNTRY_URL
        
        if self.siteyeBaglantiVarMi(url):
            url = url
        else:
            url = DiyanetUlkeler.COUNTRY_URL_NEW
        
        try:
            response = requests.get(url=url, params={"countryCode" : DiyanetUlkeler.ulkeler.get(self.ulke)})
            veriler = json.loads(response.text)
            
            sehirler = {}
            
            for i in range(0, len(veriler), 1):
                sehirler.__setitem__(veriler[i].get("Text"), veriler[i].get("Value"))
                
            self.settings = QtCore.QSettings(SehirleriAl.ayarDosyasi, QtCore.QSettings.IniFormat)
            self.settings.setValue("Diyanet/sehirler", sehirler)
        except:
            sehirler = None
            
        return sehirler