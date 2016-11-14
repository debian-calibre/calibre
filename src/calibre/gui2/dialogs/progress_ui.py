# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kovid/work/calibre/src/calibre/gui2/dialogs/progress.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(712, 308)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(I("jobs.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.title = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setWordWrap(True)
        self.title.setObjectName("title")
        self.gridLayout.addWidget(self.title, 0, 0, 1, 1)
        self.bar = QtWidgets.QProgressBar(Dialog)
        self.bar.setProperty("value", 0)
        self.bar.setObjectName("bar")
        self.gridLayout.addWidget(self.bar, 1, 0, 1, 1)
        self.message = QtWidgets.QLabel(Dialog)
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.message.setWordWrap(True)
        self.message.setObjectName("message")
        self.gridLayout.addWidget(self.message, 2, 0, 1, 1)
        self.button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Abort)
        self.button_box.setObjectName("button_box")
        self.gridLayout.addWidget(self.button_box, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):

        Dialog.setWindowTitle(_("Dialog"))
        self.title.setText(_("TextLabel"))
        self.message.setText(_("TextLabel"))


