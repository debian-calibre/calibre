# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/wizard/stanza.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(530, 316)
        self.verticalLayout = QtWidgets.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(WizardPage)
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.content_server = QtWidgets.QCheckBox(WizardPage)
        self.content_server.setObjectName("content_server")
        self.verticalLayout.addWidget(self.content_server)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.instructions = QtWidgets.QLabel(WizardPage)
        self.instructions.setWordWrap(True)
        self.instructions.setObjectName("instructions")
        self.verticalLayout.addWidget(self.instructions)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):

        WizardPage.setWindowTitle(_("WizardPage"))
        WizardPage.setTitle(_("Welcome to calibre"))
        WizardPage.setSubTitle(_("The one stop solution to all your e-book needs."))
        self.label.setText(_("<p>If you use the <a href=\"http://www.appstafarian.com/marvin.html\">Marvin</a> e-book reading app (or similar OPDS enabled apps) on your Apple iDevice, you can access your calibre book collection wirelessly, directly on the device. To do this you have to turn on the calibre Content server."))
        self.content_server.setText(_("Turn on the &Content server"))
        self.instructions.setText(_("<p>Remember to leave calibre running as the server only runs as long as calibre is running.\n"
"<p>The reader app should see your calibre collection automatically. If not, try adding the URL http://myhostname:8080 as a new catalog in the reader on your iDevice. Here myhostname should be the fully qualified hostname or the IP address of the computer calibre is running on. See <a href=\"%s\">the User Manual</a> for more information."))

