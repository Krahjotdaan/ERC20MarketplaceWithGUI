# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'application/gui/TxBrowser.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TxBrowser(object):
    def setupUi(self, TxBrowser):
        TxBrowser.setObjectName("TxBrowser")
        TxBrowser.resize(954, 168)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TxBrowser.sizePolicy().hasHeightForWidth())
        TxBrowser.setSizePolicy(sizePolicy)
        TxBrowser.setWindowTitle("")
        self.centralwidget = QtWidgets.QWidget(TxBrowser)
        self.centralwidget.setObjectName("centralwidget")
        self.tx_info = QtWidgets.QTextBrowser(self.centralwidget)
        self.tx_info.setEnabled(True)
        self.tx_info.setGeometry(QtCore.QRect(10, 10, 931, 131))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.tx_info.sizePolicy().hasHeightForWidth())
        self.tx_info.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 239, 239))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.tx_info.setPalette(palette)
        self.tx_info.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tx_info.setAcceptDrops(False)
        self.tx_info.setAutoFillBackground(False)
        self.tx_info.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tx_info.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tx_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tx_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tx_info.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tx_info.setReadOnly(True)
        self.tx_info.setObjectName("tx_info")
        TxBrowser.setCentralWidget(self.centralwidget)

        self.retranslateUi(TxBrowser)
        QtCore.QMetaObject.connectSlotsByName(TxBrowser)

    def retranslateUi(self, TxBrowser):
        _translate = QtCore.QCoreApplication.translate
        self.tx_info.setHtml(_translate("TxBrowser", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:14pt;\">Хэш транзакции: 0xc67caab0e0cd0820ab2c63fe4ac822b87c0ca8ba082adbcb7f1016d76742e13c</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:14pt;\">Полная информация: </span><span style=\" font-family:\'Consolas,Courier New,monospace\'; font-size:14pt; color:#000000;\">https://holesky.etherscan.io/tx/0xc67caab0e0cd0820ab2c63fe4ac822b87c0ca8ba082adbcb7f1016d76742e13c</span></p></body></html>"))
