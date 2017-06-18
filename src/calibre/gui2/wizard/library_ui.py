# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/wizard/library.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(481, 300)
        self.gridLayout = QtWidgets.QGridLayout(WizardPage)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(WizardPage)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.language = QtWidgets.QComboBox(WizardPage)
        self.language.setObjectName("language")
        self.gridLayout.addWidget(self.language, 0, 1, 1, 2)
        self.libloc_label1 = QtWidgets.QLabel(WizardPage)
        self.libloc_label1.setWordWrap(True)
        self.libloc_label1.setObjectName("libloc_label1")
        self.gridLayout.addWidget(self.libloc_label1, 2, 0, 1, 3)
        self.location = QtWidgets.QLineEdit(WizardPage)
        self.location.setReadOnly(True)
        self.location.setObjectName("location")
        self.gridLayout.addWidget(self.location, 3, 0, 1, 2)
        self.button_change = QtWidgets.QPushButton(WizardPage)
        self.button_change.setObjectName("button_change")
        self.gridLayout.addWidget(self.button_change, 3, 2, 1, 1)
        self.libloc_label2 = QtWidgets.QLabel(WizardPage)
        self.libloc_label2.setWordWrap(True)
        self.libloc_label2.setObjectName("libloc_label2")
        self.gridLayout.addWidget(self.libloc_label2, 4, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 1)
        self.label_3.setBuddy(self.language)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):

        WizardPage.setWindowTitle(_("WizardPage"))
        WizardPage.setTitle(_("Welcome to calibre"))
        WizardPage.setSubTitle(_("The one stop solution to all your e-book needs."))
        self.label_3.setText(_("Choose your &language:"))
        self.libloc_label1.setText(_("<p>Choose a location for your books. When you add books to calibre, they will be copied here. Use an <b>empty folder</b> for a new calibre library:"))
        self.button_change.setText(_("&Change"))
        self.libloc_label2.setText(_("If a calibre library already exists at the new location, calibre will use it automatically."))

