# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/wizard/finish.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WizardPage(object):
    def setupUi(self, WizardPage):
        WizardPage.setObjectName("WizardPage")
        WizardPage.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(WizardPage)
        self.verticalLayout.setObjectName("verticalLayout")
        self.finish_text = QtWidgets.QLabel(WizardPage)
        self.finish_text.setWordWrap(True)
        self.finish_text.setObjectName("finish_text")
        self.verticalLayout.addWidget(self.finish_text)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(WizardPage)
        self.label_2.setWordWrap(True)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.um_label = QtWidgets.QLabel(WizardPage)
        self.um_label.setWordWrap(True)
        self.um_label.setOpenExternalLinks(True)
        self.um_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard|QtCore.Qt.LinksAccessibleByMouse)
        self.um_label.setObjectName("um_label")
        self.verticalLayout.addWidget(self.um_label)

        self.retranslateUi(WizardPage)
        QtCore.QMetaObject.connectSlotsByName(WizardPage)

    def retranslateUi(self, WizardPage):

        WizardPage.setWindowTitle(_("WizardPage"))
        WizardPage.setTitle(_("Welcome to calibre"))
        WizardPage.setSubTitle(_("The one stop solution to all your e-book needs."))
        self.finish_text.setText(_("<h2>Congratulations!</h2> You have successfully setup calibre. Press the %s button to apply your settings."))
        self.label_2.setText(_("<h2>Demo videos</h2>Videos demonstrating the various features of calibre are available <a href=\"https://calibre-ebook.com/demo\">online</a>."))
        self.um_label.setText(_("<h2>User Manual</h2>A User Manual is also available <a href=\"%s\">online</a>."))

