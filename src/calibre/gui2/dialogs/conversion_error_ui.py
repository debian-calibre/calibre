# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/conversion_error.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConversionErrorDialog(object):
    def setupUi(self, ConversionErrorDialog):
        ConversionErrorDialog.setObjectName("ConversionErrorDialog")
        ConversionErrorDialog.resize(658, 515)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("lt.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConversionErrorDialog.setWindowIcon(icon)
        self.gridlayout = QtWidgets.QGridLayout(ConversionErrorDialog)
        self.gridlayout.setObjectName("gridlayout")
        self.label = QtWidgets.QLabel(ConversionErrorDialog)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(I("dialog_error.png")))
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.text = QtWidgets.QTextBrowser(ConversionErrorDialog)
        self.text.setObjectName("text")
        self.gridlayout.addWidget(self.text, 0, 1, 2, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ConversionErrorDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 2, 1, 1, 1)

        self.retranslateUi(ConversionErrorDialog)
        self.buttonBox.accepted.connect(ConversionErrorDialog.accept)
        self.buttonBox.rejected.connect(ConversionErrorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConversionErrorDialog)

    def retranslateUi(self, ConversionErrorDialog):

        ConversionErrorDialog.setWindowTitle(_("ERROR"))


