# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/password.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 209)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("mimetypes/unknown.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridlayout = QtWidgets.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")
        self.msg = QtWidgets.QLabel(Dialog)
        self.msg.setWordWrap(True)
        self.msg.setOpenExternalLinks(True)
        self.msg.setObjectName("msg")
        self.gridlayout.addWidget(self.msg, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 1, 0, 1, 1)
        self.gui_username = QtWidgets.QLineEdit(Dialog)
        self.gui_username.setObjectName("gui_username")
        self.gridlayout.addWidget(self.gui_username, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.gui_password = QtWidgets.QLineEdit(Dialog)
        self.gui_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.gui_password.setObjectName("gui_password")
        self.gridlayout.addWidget(self.gui_password, 2, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 4, 1, 1, 1)
        self.show_password = QtWidgets.QCheckBox(Dialog)
        self.show_password.setObjectName("show_password")
        self.gridlayout.addWidget(self.show_password, 3, 1, 1, 1)
        self.label.setBuddy(self.gui_username)
        self.label_2.setBuddy(self.gui_password)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Password needed"))
        self.msg.setText(_("TextLabel"))
        self.label.setText(_("&Username:"))
        self.label_2.setText(_("&Password:"))
        self.show_password.setText(_("&Show password"))


