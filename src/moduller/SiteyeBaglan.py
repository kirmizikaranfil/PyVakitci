# -*- coding: utf-8 -*-

# Hazırlayan : Rahman Yazgan (rahmanyazgan@gmail.com)
# Lisans : GPL v.3

import threading
import urllib.request

class SiteyeBaglan(threading.Thread):
    baglantiVarmi = False

    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        try:
            urllib.request.urlopen(self.url)
            SiteyeBaglan.baglantiVarmi = True
        except:
            print(self.url + " sitesine bağlantı yok.")
            SiteyeBaglan.baglantiVarmi = False