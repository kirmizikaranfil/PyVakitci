# -*- coding: utf-8 -*-

# Hazırlayan : Rahman Yazgan (rahmanyazgan@gmail.com)
# Lisans : GPL v.3

import json, requests
from PyQt4 import QtCore
from moduller.SiteyeBaglan import SiteyeBaglan
from moduller.DiyanetUlkeler import DiyanetUlkeler

class IlceleriAl:
    ayarDosyasi = None
    
    def __init__(self, sehirlerListesi, ulke, sehir):
        self.sehirler = sehirlerListesi
        self.ulke = ulke
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
        url = DiyanetUlkeler.REQUEST_URL
        
        ilceler = None
        
        if self.siteyeBaglantiVarMi(url):       
            try:
                response = requests.get(url= url , 
                                        params={"ChangeType" : "state", 
                                                "CountryId" : DiyanetUlkeler.ulkeler.get(self.ulke),
                                                "StateId" : self.sehirler.get(self.sehir)})
                veriler = json.loads(response.text)
                
                ilceler = {}
                linkler = {}
                
                for i in range(0, len(veriler["StateRegionList"]), 1):
                    ilceler.__setitem__(veriler["StateRegionList"][i].get("IlceAdi"), veriler["StateRegionList"][i].get("IlceID"))
                    linkler.__setitem__(veriler["StateRegionList"][i].get("IlceAdi"), veriler["StateRegionList"][i].get("IlceUrl"))
                
                self.settings = QtCore.QSettings(IlceleriAl.ayarDosyasi, QtCore.QSettings.IniFormat)
                self.settings.setValue("Diyanet/ilceler", ilceler)
                self.settings.setValue("Diyanet/linkler", linkler)
        
            except:
                ilceler = None
                linkler = None
        
        return ilceler, linkler