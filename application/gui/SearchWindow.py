# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'application/gui/SearchWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SearchWindow(object):
    def setupUi(self, SearchWindow):
        SearchWindow.setObjectName("SearchWindow")
        SearchWindow.setWindowModality(QtCore.Qt.WindowModal)
        SearchWindow.resize(904, 123)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SearchWindow.sizePolicy().hasHeightForWidth())
        SearchWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(SearchWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.search_type = QtWidgets.QTabWidget(self.centralwidget)
        self.search_type.setGeometry(QtCore.QRect(10, 10, 891, 221))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_type.sizePolicy().hasHeightForWidth())
        self.search_type.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.search_type.setFont(font)
        self.search_type.setObjectName("search_type")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.by_id_input = QtWidgets.QLineEdit(self.tab)
        self.by_id_input.setGeometry(QtCore.QRect(120, 10, 651, 41))
        self.by_id_input.setObjectName("by_id_input")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 41))
        self.label.setObjectName("label")
        self.by_id_button = QtWidgets.QPushButton(self.tab)
        self.by_id_button.setGeometry(QtCore.QRect(780, 10, 101, 41))
        self.by_id_button.setObjectName("by_id_button")
        self.search_type.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 141, 41))
        self.label_2.setObjectName("label_2")
        self.by_address_button = QtWidgets.QPushButton(self.tab_2)
        self.by_address_button.setGeometry(QtCore.QRect(780, 10, 101, 41))
        self.by_address_button.setObjectName("by_address_button")
        self.by_address_input = QtWidgets.QLineEdit(self.tab_2)
        self.by_address_input.setGeometry(QtCore.QRect(160, 10, 611, 41))
        self.by_address_input.setObjectName("by_address_input")
        self.search_type.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.by_name_button = QtWidgets.QPushButton(self.tab_3)
        self.by_name_button.setGeometry(QtCore.QRect(780, 10, 101, 41))
        self.by_name_button.setObjectName("by_name_button")
        self.by_name_input = QtWidgets.QLineEdit(self.tab_3)
        self.by_name_input.setGeometry(QtCore.QRect(190, 10, 581, 41))
        self.by_name_input.setObjectName("by_name_input")
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 181, 41))
        self.label_3.setObjectName("label_3")
        self.search_type.addTab(self.tab_3, "")

        self.by_id_button.clicked.connect(SearchWindow.by_id_button_click)
        self.by_address_button.clicked.connect(SearchWindow.by_address_button_click)
        self.by_name_button.clicked.connect(SearchWindow.by_name_button_click)

        SearchWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SearchWindow)
        self.search_type.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SearchWindow)

    def retranslateUi(self, SearchWindow):
        _translate = QtCore.QCoreApplication.translate
        SearchWindow.setWindowTitle(_translate("SearchWindow", "Поиск"))
        self.label.setText(_translate("SearchWindow", "Введите id:"))
        self.by_id_button.setText(_translate("SearchWindow", "Найти"))
        self.search_type.setTabText(self.search_type.indexOf(self.tab), _translate("SearchWindow", "По id"))
        self.label_2.setText(_translate("SearchWindow", "Введите адрес:"))
        self.by_address_button.setText(_translate("SearchWindow", "Найти"))
        self.search_type.setTabText(self.search_type.indexOf(self.tab_2), _translate("SearchWindow", "По адресу токена"))
        self.by_name_button.setText(_translate("SearchWindow", "Найти"))
        self.label_3.setText(_translate("SearchWindow", "Введите название:"))
        self.search_type.setTabText(self.search_type.indexOf(self.tab_3), _translate("SearchWindow", "По названию"))
