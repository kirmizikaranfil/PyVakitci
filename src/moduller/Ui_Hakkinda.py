# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Hakkinda.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(418, 231)
        Dialog.setMinimumSize(QtCore.QSize(418, 231))
        Dialog.setMaximumSize(QtCore.QSize(418, 231))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        Dialog.setFont(font)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 401, 211))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.hakkinda_tab = QtWidgets.QWidget()
        self.hakkinda_tab.setObjectName("hakkinda_tab")
        self.hakkinda_label = QtWidgets.QLabel(self.hakkinda_tab)
        self.hakkinda_label.setGeometry(QtCore.QRect(10, 10, 381, 171))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.hakkinda_label.setFont(font)
        self.hakkinda_label.setObjectName("hakkinda_label")
        self.tabWidget.addTab(self.hakkinda_tab, "")
        self.yazar_tab = QtWidgets.QWidget()
        self.yazar_tab.setObjectName("yazar_tab")
        self.yazar_label = QtWidgets.QLabel(self.yazar_tab)
        self.yazar_label.setGeometry(QtCore.QRect(10, 10, 381, 171))
        self.yazar_label.setObjectName("yazar_label")
        self.tabWidget.addTab(self.yazar_tab, "")
        self.hata_bildirimi_tab = QtWidgets.QWidget()
        self.hata_bildirimi_tab.setObjectName("hata_bildirimi_tab")
        self.hata_bildirimi_label = QtWidgets.QLabel(self.hata_bildirimi_tab)
        self.hata_bildirimi_label.setGeometry(QtCore.QRect(10, 10, 391, 171))
        self.hata_bildirimi_label.setObjectName("hata_bildirimi_label")
        self.tabWidget.addTab(self.hata_bildirimi_tab, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Hakkında"))
        self.hakkinda_label.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">PyVakitci 1.7</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\';\">Diyanet verilerine göre tüm ülke ve şehirler için namaz </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\';\">vakitlerini gösterir. İsteğe bağlı olarak namaz vaktinde </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\';\">ezan ve ezan duasını okur.</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans\';\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\';\">Ezan için kullanılan ses dosyaları İsmail COŞAR\'a aittir. </span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans\';\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Sans\';\"> </span><a href=\"https://sourceforge.net/projects/pyvakitci2011\"><span style=\" font-family:\'Sans\'; text-decoration: underline; color:#0000ff;\">https://sourceforge.net/projects/pyvakitci2011</span></a></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.hakkinda_tab), _translate("Dialog", "Hakkında"))
        self.yazar_label.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt;\">Rahman YAZGAN</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"mailto:rahmanyazgan@gmail.com\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; text-decoration: underline; color:#0000ff;\">rahmanyazgan@gmail.com</span></a></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.yazar_tab), _translate("Dialog", "Yazar"))
        self.hata_bildirimi_label.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt;\">Hataları bildirmek veya programa katkıda </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt;\">bulunmak için  </span><a href=\"mailto:rahmanyazgan@gmail.com\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; text-decoration: underline; color:#0000ff;\">rahmanyazgan@gmail.com</span></a><span style=\" font-family:\'Sans\'; font-size:12pt;\"> </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt;\">adresini kullanabilirsiniz.</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.hata_bildirimi_tab), _translate("Dialog", "Hata Bildirimi ve Destek"))
