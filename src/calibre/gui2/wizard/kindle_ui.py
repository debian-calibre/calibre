# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/wizard/kindle.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(WizardPage)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(WizardPage)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(True)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(WizardPage)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.to_address = QtWidgets.QLineEdit(WizardPage)
        self.to_address.setObjectName("to_address")
        self.gridLayout.addWidget(self.to_address, 1, 1, 1, 1)
        self.send_email_widget = SendEmail(WizardPage)
        self.send_email_widget.setObjectName("send_email_widget")
        self.gridLayout.addWidget(self.send_email_widget, 2, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.label_2.setBuddy(self.to_address)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):

        WizardPage.setWindowTitle(_("WizardPage"))
        WizardPage.setTitle(_("Welcome to calibre"))
        WizardPage.setSubTitle(_("The one stop solution to all your e-book needs."))
        self.label.setText(_("<p>calibre can automatically send books by email to your Kindle. To do that you have to setup email delivery below. The easiest way is to setup a free <a href=\"https://gmx.com\">GMX account</a> and click the \"Use GMX\" button below. You will also have to register your email address in your Amazon account."))
        self.label_2.setText(_("&Kindle email:"))

from calibre.gui2.wizard.send_email import SendEmail
