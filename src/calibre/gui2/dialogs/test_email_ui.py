# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/test_email.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(542, 418)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("config.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.from_ = QtWidgets.QLabel(Dialog)
        self.from_.setWordWrap(True)
        self.from_.setObjectName("from_")
        self.verticalLayout.addWidget(self.from_)
        self.to = QtWidgets.QLineEdit(Dialog)
        self.to.setObjectName("to")
        self.verticalLayout.addWidget(self.to)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setText("")
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.test_button = QtWidgets.QPushButton(Dialog)
        self.test_button.setObjectName("test_button")
        self.verticalLayout.addWidget(self.test_button)
        self.log = QtWidgets.QPlainTextEdit(Dialog)
        self.log.setObjectName("log")
        self.verticalLayout.addWidget(self.log)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Test email settings"))
        self.from_.setText(_("Send test mail from %s to:"))
        self.test_button.setText(_("&Test"))


